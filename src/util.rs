#[cfg(feature = "fxhash")]
pub type Hasher = std::hash::BuildHasherDefault<rustc_hash::FxHasher>;

#[cfg(not(feature = "fxhash"))]
pub type Hasher = std::collections::hash_map::RandomState;
