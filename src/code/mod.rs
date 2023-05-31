use std::borrow::Cow;
use std::cell::RefCell;
use std::io;
use std::io::Write;
use std::rc::Rc;

/// A `CodeBuffer` is a buffer that can be used to generate code without having
/// to keep track of identation. A `CodeBuffer` contains either plain text which
/// will be indented accoridng to the buffer's own indent, or nested
/// `CodeBuffer`s which will be intended according to their own indent, on top
/// of the containing buffer's indent.
pub struct CodeBuffer {
    indent: Cow<'static, str>,
    content: RefCell<Vec<CodeBufferContent>>,
}

impl CodeBuffer {
    /// Creates a new `CodeBuffer` with no identation.
    pub const fn new() -> Self {
        Self::with_indent(Cow::Borrowed(""))
    }

    /// Adds a single newline character to this code buffer.
    #[inline]
    pub fn newline(&self) {
        self.line(Cow::Borrowed(""))
    }

    /// Adds text into the buffer, followed by a new line.
    pub fn line(&self, text: impl Into<Cow<'static, str>>) {
        let mut content = self.content.borrow_mut();
        content.push(CodeBufferContent::String(text.into(), true));
    }

    /// Adds text into the buffer, as-is.
    pub fn text(&self, text: impl Into<Cow<'static, str>>) {
        let mut content = self.content.borrow_mut();
        content.push(CodeBufferContent::String(text.into(), false));
    }

    /// Creates a new indented sub-buffer at the current position.
    #[inline]
    pub fn indent(&self, indent: Cow<'static, str>) -> Rc<CodeBuffer> {
        self.indent_with_options(IndentOptions {
            indent,
            leading: None,
            trailing: None,
            trailing_newline: false,
        })
    }

    /// Creates a new indented sub-buffer at the current position.
    pub fn indent_with_options(&self, options: IndentOptions) -> Rc<CodeBuffer> {
        let mut content = self.content.borrow_mut();
        if let Some(leading) = options.leading {
            content.push(CodeBufferContent::String(leading, true));
        }

        let idx = content.len();
        content.push(CodeBufferContent::Buffer(Rc::new(CodeBuffer::with_indent(
            Cow::Owned(format!("{}{}", self.indent, options.indent)),
        ))));

        if let Some(trailing) = options.trailing {
            content.push(CodeBufferContent::String(
                trailing,
                options.trailing_newline,
            ));
        } else if options.trailing_newline {
            content.push(CodeBufferContent::String(Cow::Borrowed(""), true));
        }

        content[idx].as_buffer()
    }

    /// Creates a new un-indented sub-buffer at the current position.
    #[inline]
    pub fn section(&self, trailing_newline: bool) -> Rc<CodeBuffer> {
        self.indent_with_options(IndentOptions {
            indent: Cow::Borrowed(""),
            leading: None,
            trailing: None,
            trailing_newline,
        })
    }

    /// Writes the content of this `CodeBuffer` into the provided writer.
    pub fn write(self, writer: &mut dyn io::Write) -> io::Result<()> {
        self.inner_write(&mut IndentedWriter::new(writer))
    }

    fn inner_write(&self, writer: &mut IndentedWriter) -> io::Result<()> {
        writer.with_indent(&self.indent, move |writer| {
            for item in self.content.borrow().iter() {
                item.write(writer)?;
            }
            Ok(())
        })
    }
}

impl CodeBuffer {
    const fn with_indent(indent: Cow<'static, str>) -> Self {
        Self {
            indent,
            content: RefCell::new(Vec::new()),
        }
    }
}

impl Default for CodeBuffer {
    #[inline(always)]
    fn default() -> Self {
        Self::new()
    }
}

/// Options for creating indented blocks.
pub struct IndentOptions {
    /// The indentation to add to the current indentation.
    pub indent: Cow<'static, str>,
    /// The text to add before the indented block begins. It'll be suffixed with
    /// a newline character.
    pub leading: Option<Cow<'static, str>>,
    /// The text to add after the indentated block ends.
    pub trailing: Option<Cow<'static, str>>,
    /// Whether a newline should be inserted after the block ends (after the
    /// trailing, if one is provided).
    pub trailing_newline: bool,
}

enum CodeBufferContent {
    String(Cow<'static, str>, bool),
    Buffer(Rc<CodeBuffer>),
}

impl CodeBufferContent {
    fn as_buffer(&self) -> Rc<CodeBuffer> {
        match self {
            Self::Buffer(buffer) => buffer.clone(),
            _ => unreachable!("expected a buffer"),
        }
    }

    fn write(&self, writer: &mut IndentedWriter) -> io::Result<()> {
        match self {
            Self::String(string, newline) => {
                if *newline {
                    writeln!(writer, "{string}")
                } else {
                    write!(writer, "{string}")
                }
            }
            Self::Buffer(buffer) => buffer.inner_write(writer),
        }
    }
}

struct IndentedWriter<'a> {
    indent: &'a [u8],
    writer: &'a mut dyn io::Write,

    after_newline: bool,
}

impl<'a> IndentedWriter<'a> {
    fn new(writer: &'a mut dyn io::Write) -> Self {
        Self {
            indent: &[],
            writer,
            after_newline: true,
        }
    }

    fn with_indent(
        &mut self,
        indent: &str,
        cb: impl FnOnce(&mut IndentedWriter<'_>) -> io::Result<()>,
    ) -> io::Result<()> {
        let mut delegate = IndentedWriter {
            indent: indent.as_bytes(),
            writer: self.writer,
            after_newline: self.after_newline,
        };

        let result = cb(&mut delegate);
        self.after_newline = delegate.after_newline;
        result
    }
}

impl io::Write for IndentedWriter<'_> {
    fn write(&mut self, mut buf: &[u8]) -> io::Result<usize> {
        // Short-circuit to the raw writer if there is no indentation.
        if self.indent.is_empty() {
            return self.writer.write(buf);
        }

        let mut written = 0;
        while !buf.is_empty() {
            let (slice, nl) = match buf.iter().position(|&b| b == b'\n') {
                None => (buf, false),
                Some(idx) => (&buf[..=idx], true),
            };
            debug_assert!(!slice.is_empty(), "the slice cannot be empty");

            if self.after_newline && (slice.len() > 1 || !nl) {
                // Note: this does not count as written output here...
                self.writer.write_all(self.indent)?;
                self.after_newline = false;
            }

            let out = self.writer.write(slice)?;
            written += out;

            if out < slice.len() {
                // We couldn't write it all, so we'll return here...
                break;
            }

            self.after_newline = nl;
            buf = &buf[slice.len()..];
        }

        Ok(written)
    }

    #[inline]
    fn flush(&mut self) -> io::Result<()> {
        self.writer.flush()
    }
}
