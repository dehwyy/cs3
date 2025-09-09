#[derive(Default)]
pub struct Text {
    pub(super) inner: String,
    pub(super) author: Option<String>,
    pub(super) headline: Option<String>,
}

impl std::fmt::Display for Text {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if let Some(author) = &self.author {
            write!(f, "{}\n", author)?;
        }

        if let Some(headline) = &self.headline {
            write!(f, "{}\n", headline)?;
        }

        write!(f, "{}", self.inner)
    }
}
