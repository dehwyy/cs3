pub mod sber;
pub mod tbank;
pub mod test;
pub mod types;

use types::*;

pub trait Adapter {
    fn CreateTransaction(
        &mut self,
        payload: CreateTransactionPayload,
    ) -> Result<Transaction, String>;

    fn FinalizeTransaction(&mut self, payload: FinalizeTransactionPayload) -> Result<(), String>;
}
