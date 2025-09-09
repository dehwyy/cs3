pub use super::{Adapter, sber::*, tbank::*, types::*};

#[cfg(test)]
mod tests {
    use super::*;
    use uuid::Uuid;

    fn make_adapter() -> TBank {
        TBank::new()
    }

    #[test]
    fn create_transaction_card_ok() {
        let mut bank = make_adapter();

        let tx = bank
            .CreateTransaction(CreateTransactionPayload {
                requested_sum: 1234.56,
                payee_kind: PayeeKind::Card,
            })
            .expect("must create");

        assert!(!tx.id.is_empty());
        assert_eq!(tx.sum, 1234.56);
        match tx.payee_account {
            PayeeAccount::Card { ref bank, .. } => assert_eq!(bank, "TBank"),
            _ => panic!("expected card account"),
        }

        // Внутреннее состояние должно содержать статус New
        let id = Uuid::parse_str(&tx.id).unwrap();
        assert!(matches!(
            bank.transactions.get(&id),
            Some(TransactionState::New)
        ));
    }

    #[test]
    fn create_transaction_sbp_ok() {
        let mut bank = make_adapter();

        let tx = bank
            .CreateTransaction(CreateTransactionPayload {
                requested_sum: 10.0,
                payee_kind: PayeeKind::Sbp,
            })
            .expect("must create");

        match tx.payee_account {
            PayeeAccount::Sbp {
                ref bank,
                ref owner_name,
                ..
            } => {
                assert_eq!(bank, "TBank");
                assert_eq!(owner_name, "Petr Petrov");
            }
            _ => panic!("expected sbp account"),
        }
    }

    #[test]
    fn finalize_transaction_success_updates_state() {
        let mut bank = make_adapter();

        let tx = bank
            .CreateTransaction(CreateTransactionPayload {
                requested_sum: 50.0,
                payee_kind: PayeeKind::Card,
            })
            .unwrap();

        bank.FinalizeTransaction(FinalizeTransactionPayload {
            id: tx.id.clone(),
            new_state: TransactionState::Success,
        })
        .expect("finalize ok");

        let id = Uuid::parse_str(&tx.id).unwrap();
        assert!(matches!(
            bank.transactions.get(&id),
            Some(TransactionState::Success)
        ));
    }

    #[test]
    fn finalize_transaction_with_invalid_uuid_fails() {
        let mut bank = make_adapter();

        let err = bank
            .FinalizeTransaction(FinalizeTransactionPayload {
                id: "not-a-uuid".to_string(),
                new_state: TransactionState::Failed,
            })
            .expect_err("should fail");

        assert!(
            err.contains("invalid length") || err.contains("ParseError") || err.contains("invalid")
        );
    }

    #[test]
    fn finalize_transaction_not_found_fails() {
        let mut bank = make_adapter();
        let random_id = Uuid::new_v4().to_string();

        let err = bank
            .FinalizeTransaction(FinalizeTransactionPayload {
                id: random_id,
                new_state: TransactionState::Cancelled,
            })
            .expect_err("should fail, no such tx");

        assert_eq!(err, "Transaction not found");
    }
}
