use super::{Adapter, types::*};
use std::collections::HashMap;
use uuid::Uuid;

pub struct TBank {
    pub transactions: HashMap<Uuid, TransactionState>,
}

impl TBank {
    pub fn new() -> Self {
        Self {
            transactions: HashMap::new(),
        }
    }

    pub fn GetFreeCard(&self) -> Option<PayeeAccount> {
        Some(PayeeAccount::Card {
            card_number: String::from("5536 9100 0000 0000"),
            bank: String::from("TBank"),
        })
    }

    pub fn GetFreeSBP(&self) -> Option<PayeeAccount> {
        Some(PayeeAccount::Sbp {
            sbp_number: String::from("+7 900 111-22-33"),
            bank: String::from("TBank"),
            owner_name: String::from("Petr Petrov"),
        })
    }

    /// Returns new transaction id
    pub fn NewPayment(&mut self) -> Result<Uuid, String> {
        println!("TBank initiate payment");
        let id = Uuid::new_v4();
        if let Some(_) = self.transactions.insert(id, TransactionState::New) {
            return Err(String::from("Transaction already exists"));
        }
        Ok(id)
    }

    pub fn UpdatePayment(&mut self, id: &Uuid, state: TransactionState) -> Result<(), String> {
        println!("TBank update payment");
        match self.transactions.get_mut(id) {
            Some(v) => {
                *v = state;
                Ok(())
            }
            None => Err(String::from("Transaction not found")),
        }
    }
}

impl Adapter for TBank {
    fn CreateTransaction(
        &mut self,
        payload: CreateTransactionPayload,
    ) -> Result<Transaction, String> {
        let payee_account = match payload.payee_kind {
            PayeeKind::Card => self.GetFreeCard(),
            PayeeKind::Sbp => self.GetFreeSBP(),
        };

        if payee_account.is_none() {
            return Err(String::from("Payee account not found"));
        }

        let tx_id = self.NewPayment().map_err(|err| {
            eprintln!("{}", err);
            err
        })?;

        Ok(Transaction {
            id: tx_id.to_string(),
            sum: payload.requested_sum,
            payee_account: payee_account.unwrap(),
        })
    }

    fn FinalizeTransaction(&mut self, payload: FinalizeTransactionPayload) -> Result<(), String> {
        let parsed_id = uuid::Uuid::parse_str(&payload.id).map_err(|err| err.to_string())?;
        self.UpdatePayment(&parsed_id, payload.new_state)
    }
}
