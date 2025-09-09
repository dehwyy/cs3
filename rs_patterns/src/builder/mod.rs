pub mod r#macro;
pub mod text;
pub mod text_builder;

#[cfg(test)]
mod tests {
    use super::text::Text;
    use super::text_builder::TextBuilder;
    use std::fmt::Write as _;

    // -------- Helper pipes (fn pointers, не замыкания) --------
    fn trim_pipe(s: String) -> String {
        s.trim().to_string()
    }
    fn upper_pipe(s: String) -> String {
        s.to_uppercase()
    }
    fn add_bang_pipe(s: String) -> String {
        format!("{s}!")
    }

    #[test]
    fn build_minimal_empty_by_default() {
        let t = TextBuilder::new().build();
        assert_eq!(t.to_string(), "");
    }

    #[test]
    fn build_with_text_only_no_pipes() {
        let t = TextBuilder::new().with_text("hello".into()).build();

        assert_eq!(t.to_string(), "hello");
    }

    #[test]
    fn build_with_author_and_headline_and_text() {
        let t = TextBuilder::new()
            .with_author("Author Name".into())
            .with_headline("Breaking Headline".into())
            .with_text("Body".into())
            .build();

        // Ожидаемый формат Display:
        // author\n
        // headline\n
        // inner
        assert_eq!(t.to_string(), "Author Name\nBreaking Headline\nBody");
    }

    #[test]
    fn display_with_only_author() {
        let t = TextBuilder::new()
            .with_author("Only Author".into())
            .with_text("Body".into())
            .build();

        assert_eq!(t.to_string(), "Only Author\nBody");
    }

    #[test]
    fn display_with_only_headline() {
        let t = TextBuilder::new()
            .with_headline("Only Headline".into())
            .with_text("Body".into())
            .build();

        assert_eq!(t.to_string(), "Only Headline\nBody");
    }

    #[test]
    fn pipes_apply_in_insertion_order() {
        // Текст с пробелами вокруг -> trim -> upper -> add !
        let t = TextBuilder::new()
            .with_text("  hello world  ".into())
            .with_pipe(trim_pipe)
            .with_pipe(upper_pipe)
            .with_pipe(add_bang_pipe)
            .build();

        assert_eq!(t.to_string(), "HELLO WORLD!");
    }

    #[test]
    fn with_appended_text_accumulates_before_pipes() {
        let t = TextBuilder::new()
            .with_text("foo".into())
            .with_appended_text("bar".into())
            .with_pipe(upper_pipe)
            .build();

        // "foobar" -> upper -> "FOOBAR"
        assert_eq!(t.to_string(), "FOOBAR");
    }

    #[test]
    fn display_exact_newline_placement() {
        let t = TextBuilder::new()
            .with_author("A".into())
            .with_headline("H".into())
            .with_text("X".into())
            .build();

        // Проверим точную расстановку переносов строк
        let mut expected = String::new();
        write!(&mut expected, "A\nH\nX").unwrap();

        assert_eq!(t.to_string(), expected);
    }

    #[test]
    fn pipes_on_empty_text_are_ok() {
        let t = TextBuilder::new()
            .with_pipe(add_bang_pipe) // "" -> "!"
            .build();

        assert_eq!(t.to_string(), "!");
    }

    #[test]
    fn multiple_builders_independent_state() {
        let t1 = TextBuilder::new()
            .with_text("alpha".into())
            .with_pipe(upper_pipe)
            .build();

        let t2 = TextBuilder::new()
            .with_text("  beta  ".into())
            .with_pipe(trim_pipe)
            .build();

        assert_eq!(t1.to_string(), "ALPHA");
        assert_eq!(t2.to_string(), "beta");
    }
}
