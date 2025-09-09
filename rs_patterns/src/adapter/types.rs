pub enum PayeeKind {
    Card,
    Sbp,
}

pub enum PayeeAccount {
    Card {
        card_number: String,
        bank: String,
    },
    Sbp {
        sbp_number: String,
        bank: String,
        owner_name: String,
    },
}

pub enum TransactionState {
    New,
    Success,
    Failed,
    Cancelled,
}

pub struct Transaction {
    pub id: String,

    pub sum: f64,
    pub payee_account: PayeeAccount,
}

pub struct CreateTransactionPayload {
    pub requested_sum: f64,

    pub payee_kind: PayeeKind,
}

pub struct FinalizeTransactionPayload {
    pub id: String,

    pub new_state: TransactionState,
}
