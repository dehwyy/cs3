use crate::builder::text_builder::TextBuilder;

mod adapter;
mod builder;
mod memento;

fn main() {
    let text = TextBuilder::new()
        .with_author("Egor dehwyy".into())
        .with_headline("It's all about the style".into())
        .with_text(
            "Let's start with some text. And then some more text\nIt's all about the style".into(),
        )
        .with_pipe(|text| text.to_uppercase())
        .with_rgb(255, 40, 120) // подсветка розовым
        .build();

    println!("{}", text);
}
