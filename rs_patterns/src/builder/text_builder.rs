use crate::{builder::r#macro, styled};

use super::text;

#[derive(Default)]
pub struct TextBuilder {
    pipes: Vec<Box<dyn Fn(String) -> String>>,
    headline: Option<String>,
    author: Option<String>,
    rgb: Option<(u8, u8, u8)>,
    text: String,
}

impl TextBuilder {
    pub fn new() -> TextBuilder {
        TextBuilder::default()
    }

    pub fn with_pipe(mut self, pipe: impl Fn(String) -> String + 'static) -> Self {
        self.pipes.push(Box::new(pipe));

        self
    }

    pub fn with_headline(mut self, headline: String) -> Self {
        self.headline = Some(headline);

        self
    }

    pub fn with_author(mut self, author: String) -> Self {
        self.author = Some(author);

        self
    }

    pub fn with_text(mut self, text: String) -> Self {
        self.text = text;

        self
    }

    pub fn with_appended_text(mut self, text: String) -> Self {
        self.text += &text;

        self
    }

    pub fn with_rgb(mut self, r: u8, g: u8, b: u8) -> Self {
        self.rgb = Some((r, g, b));

        self
    }

    pub fn build(self) -> text::Text {
        let mut text = text::Text {
            inner: self.pipes.iter().fold(self.text, |text, pipe| pipe(text)),
            ..Default::default()
        };

        if let Some(author) = self.author {
            text.author = Some(styled!(format!("Author: {author}\n"), 4));
        }

        if let Some(headline) = self.headline {
            text.headline = Some(styled!(format!("Title: {headline}!\n"), 1));
        }

        if let Some((r, g, b)) = self.rgb {
            text.inner = styled!(text.inner, r, g, b);
        }

        text
    }
}
