use std::io;

pub struct CodeSink<'a> {
    config: CodeSinkConfig,
    indentation: String,
    writer: &'a mut dyn io::Write,
}

impl<'a> CodeSink<'a> {
    fn new(config: CodeSinkConfig, writer: &'a mut dyn io::Write) -> Self {
        Self {
            config,
            indentation: String::new(),
            writer,
        }
    }

    /// Creates a new CodeSink configured for emitting TypeScript.
    #[inline(always)]
    pub fn typescript(writer: &'a mut dyn io::Write) -> Self {
        Self::new(CodeSinkConfig::typescript(), writer)
    }

    /// Returns a new CodeSink indented one level deeper.
    pub fn indented(&mut self) -> CodeSink<'_> {
        let mut indentation = self.indentation.clone();
        indentation.push_str(self.config.indent);
        CodeSink {
            config: self.config,
            indentation,
            writer: self.writer,
        }
    }

    /// Writes a blank line to the underlying writer with no indentation.
    pub fn blank_line(&mut self) -> io::Result<()> {
        writeln!(self.writer)
    }

    /// Writes the provided text with optional indentiation, and no added
    /// newline at the end.
    pub fn write_raw(&mut self, text: &str, indent: bool) -> io::Result<()> {
        write!(
            self.writer,
            "{}{text}",
            if indent { &self.indentation } else { "" }
        )
    }

    /// Writes the provided text with optional indentation, and a new line added
    /// at the end.
    pub fn write_raw_line(&mut self, text: &str, indent: bool) -> io::Result<()> {
        writeln!(
            self.writer,
            "{}{text}",
            if indent { &self.indentation } else { "" }
        )
    }

    /// Writes the provided text with the correct indentation at the begining
    /// and no new line added tat the end.
    pub fn write(&mut self, text: &str) -> io::Result<()> {
        write!(self.writer, "{}{text}", self.indentation)
    }

    /// Writes a single line to the underlying writer with indentation.
    pub fn write_line(&mut self, line: &str) -> io::Result<()> {
        writeln!(self.writer, "{}{line}", self.indentation)
    }

    /// Writes the provided text out to the writer, with each line indented.
    pub fn write_text(&mut self, text: &str) -> io::Result<()> {
        for line in text.lines() {
            self.write_line(line)?;
        }
        Ok(())
    }

    /// Writes the provided text out to the writer, with each line prefixed with
    /// the provided prefix, and correctly indented.
    pub fn write_with_prefix(&mut self, prefix: &str, text: &str) -> io::Result<()> {
        for line in text.lines() {
            self.write_line(&format!("{prefix}{line}"))?;
        }
        Ok(())
    }
}

#[derive(Clone, Copy)]
struct CodeSinkConfig {
    /// The string to use for indentation.
    indent: &'static str,
}

impl CodeSinkConfig {
    const fn typescript() -> Self {
        Self { indent: "  " }
    }
}
