#[macro_export]
macro_rules! styled {
    // Do not do anything
    ($text:expr,$r:expr, $g:expr, $b:expr) => {
        format!("\x1b[38;2;{};{};{}m{}\x1b[0m", $r, $g, $b, $text)
    };
    ($text:expr,$style:expr) => {
        format!("\x1b[{}m{}\x1b[0m", $style, $text)
    };
}
