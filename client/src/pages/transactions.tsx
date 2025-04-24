import { useCallback, useEffect, useState } from "react";
import { Button, Form, InputNumber, Modal, Select } from "antd";
import { API_URL } from "../const";
import { useNavigate } from "react-router-dom";

interface TransactionFormValues {
  exchangeRate: string;
  fromWallet: string;
  toWallet: string;
  amount: number;
}

interface Wallet {
  id: string;
  name: string;
  currency: string;
  balance: number;
  created_at: string;
  updated_at: string;
}

interface WalletOption {
  value: string;
  label: string;
}

interface ExchangeRate {
  id: string;
  rate: number;
  from_currency: string;
  to_currency: string;
}

interface ExchangeRateOption {
  value: string;
  label: string;
  from_currency: string;
  to_currency: string;
}

export const TransactionsPage = () => {
  const [htmlContent, setHtmlContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();

  const [exchangeRates, setExchangeRates] = useState<ExchangeRateOption[]>([]);
  const [fromWalletOptions, setFromWalletOptions] = useState<WalletOption[]>([]);
  const [toWalletOptions, setToWalletOptions] = useState<WalletOption[]>([]);

  const fetchTransactions = useCallback(() => {
    fetch(`${API_URL}/transactions/list`, {
      method: "GET",
      credentials: "include",
    })
      .then((response) => {
        if (response.status === 401) {
          navigate("/login", { replace: true });
          return Promise.reject("Unauthorized");
        }
        return response.text();
      })
      .then((html) => {
        setHtmlContent(html);
        setLoading(false);
      })
      .catch((error) => {
        if (error !== "Unauthorized") {
          console.error("Failed to fetch transactions:", error);
        }
      });
  }, [navigate]);

  useEffect(() => {
    fetchTransactions();
  }, [fetchTransactions]);

  useEffect(() => {
    fetch(`${API_URL}/exchange-rate/reference`, {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data: { exchange_rates: ExchangeRate[] }) => {
        const options: ExchangeRateOption[] = data.exchange_rates.map((er) => ({
          value: String(er.id),
          label: `${er.from_currency} → ${er.to_currency} (${er.rate})`,
          from_currency: er.from_currency,
          to_currency: er.to_currency,
        }));
        setExchangeRates(options);
      })
      .catch((err) => console.error("Failed to load exchange rates", err));
  }, []);

  const onExchangeRateChange = (value: string) => {
    const selectedRate = exchangeRates.find((rate) => rate.value === value);
    if (!selectedRate) return;

    const { from_currency, to_currency } = selectedRate;

    fetch(`${API_URL}/wallets/reference?currency=${from_currency}`, {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data: { wallets: Wallet[] }) => {
        const options: WalletOption[] = data.wallets.map((wallet) => ({
          label: wallet.name,
          value: wallet.id,
        }));
        setFromWalletOptions(options);
      });

    fetch(`${API_URL}/wallets/reference?currency=${to_currency}`, {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data: { wallets: Wallet[] }) => {
        const options: WalletOption[] = data.wallets.map((wallet) => ({
          label: wallet.name,
          value: wallet.id,
        }));
        setToWalletOptions(options);
      });
  };

  const createTransaction = (values: TransactionFormValues) => {
    fetch(`${API_URL}/transactions/item`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        from_wallet_id: values.fromWallet,
        to_wallet_id: values.toWallet,
        amount: values.amount,
        exchange_rate_id: values.exchangeRate,
      }),
    })
      .then(() => {
        setOpen(false);
        fetchTransactions();
      })
      .catch((error) => console.error(error));
  };

  if (loading) return <div>Loading transactions...</div>;

  return (
    <>
      <div className="transactions-container">
        <Button onClick={() => setOpen(true)}>New Transaction</Button>
        <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      </div>
      <Modal
        title="New Transaction"
        open={open}
        footer={null}
        onClose={() => setOpen(false)}
        onCancel={() => setOpen(false)}
      >
        <Form<TransactionFormValues>
          layout="vertical"
          onFinish={createTransaction}
        >
          <Form.Item<TransactionFormValues>
            label="Exchange Rate"
            name="exchangeRate"
            rules={[{ required: true }]}
          >
            <Select
              placeholder="Select exchange rate"
              options={exchangeRates}
              onChange={onExchangeRateChange}
            />
          </Form.Item>

          <Form.Item<TransactionFormValues>
            label="From Wallet"
            name="fromWallet"
            rules={[{ required: true }]}
          >
            <Select placeholder="Select source wallet" options={fromWalletOptions} />
          </Form.Item>

          <Form.Item<TransactionFormValues>
            label="To Wallet"
            name="toWallet"
            rules={[{ required: true }]}
          >
            <Select placeholder="Select destination wallet" options={toWalletOptions} />
          </Form.Item>

          <Form.Item<TransactionFormValues>
            label="Buy Amount"
            name="amount"
            rules={[{ required: true }]}
          >
            <InputNumber placeholder="Amount" style={{ width: "100%" }} />
          </Form.Item>

          <Form.Item label={null}>
            <Button type="primary" htmlType="submit">
              Transfer
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};
