pub struct Memento<T: Clone> {
    last_state: Option<T>,
}

impl<T: Clone> Memento<T> {
    pub fn new() -> Self {
        Self { last_state: None }
    }

    pub fn save(&mut self, state: &T) -> () {
        self.last_state = Some(state.clone());
    }

    pub fn restore(&mut self, dist: &mut T) {
        if let Some(state) = self.last_state.take() {
            *dist = state;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::Memento;

    #[derive(Clone, PartialEq, Debug)]
    struct State {
        x: i32,
        name: String,
        data: Vec<i32>,
    }

    impl State {
        fn new(x: i32, name: &str, data: Vec<i32>) -> Self {
            Self {
                x,
                name: name.to_string(),
                data,
            }
        }
    }

    #[test]
    fn restore_without_saved_state_is_noop() {
        let mut m: Memento<State> = Memento::new();

        let original = State::new(1, "orig", vec![1, 2]);
        let mut dist = original.clone();

        m.restore(&mut dist); // ничего не сохранено — не меняет
        assert_eq!(dist, original);
    }

    #[test]
    fn save_then_restore_restores_snapshot() {
        let mut m: Memento<State> = Memento::new();

        let snap = State::new(10, "snap", vec![9, 8, 7]);
        m.save(&snap);

        let mut dist = State::new(0, "dist", vec![]);
        assert_ne!(dist, snap);

        m.restore(&mut dist);
        assert_eq!(dist, snap);
    }

    #[test]
    fn multiple_saves_last_wins() {
        let mut m: Memento<State> = Memento::new();

        let s1 = State::new(1, "one", vec![1]);
        let s2 = State::new(2, "two", vec![2, 2]);

        m.save(&s1);
        m.save(&s2);

        let mut dist = State::new(0, "z", vec![]);
        m.restore(&mut dist);

        assert_eq!(dist, s2);
    }

    #[test]
    fn restore_consumes_saved_state() {
        let mut m: Memento<State> = Memento::new();
        let snap = State::new(3, "three", vec![3, 3, 3]);

        m.save(&snap);

        let mut dist = State::new(0, "zero", vec![]);
        m.restore(&mut dist);
        assert_eq!(dist, snap);

        // Второй restore ничего не меняет (состояние было "взято" через take)
        let prev = dist.clone();
        m.restore(&mut dist);
        assert_eq!(dist, prev);
    }

    #[test]
    fn snapshot_independent_from_later_mutations() {
        let mut m: Memento<State> = Memento::new();

        let mut src = State::new(5, "before", vec![1, 2, 3]);
        m.save(&src);

        // Меняем исходник после сохранения
        src.x = 42;
        src.name = "after".to_string();
        src.data.push(99);

        let mut dist = State::new(0, "target", vec![]);
        m.restore(&mut dist);

        // Ожидаем старый снимок, а не изменённую версию
        assert_eq!(dist, State::new(5, "before", vec![1, 2, 3]));
        assert_ne!(dist, src);
    }

    #[test]
    fn works_with_plain_generic_string() {
        let mut m: Memento<String> = Memento::new();

        let snap = String::from("hello");
        m.save(&snap);

        let mut dist = String::from("xxx");
        m.restore(&mut dist);

        assert_eq!(dist, "hello");
    }
}
