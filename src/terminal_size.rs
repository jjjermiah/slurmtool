use terminal_size::{Width, Height, terminal_size};


#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TerminalSize {
    pub width: u16,
    pub height: u16,
}

impl TerminalSize {
    pub fn new(width: u16, height: u16) -> Self {
        Self { width, height }
    }

    pub fn from_terminal_size() -> Self {
        let (Width(width), Height(height)) = terminal_size().unwrap();
        Self { width, height }
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_terminal_size() {
        let terminal_size = TerminalSize::from_terminal_size();
        println!("{:?}", terminal_size);
    }
}