import { useCallback, useEffect, useState } from "react";
import { Button, Form, Input, InputNumber, Modal, Select } from "antd";
import { API_URL, currencyOptions } from "../const";
import { useNavigate } from "react-router-dom";

interface WalletFormValues {
  name: string;
  currency: string;
}

interface WalletActionsFormValues {
  walletId: string;
  type: WalletActions;
  amount: number;
}

interface WalletReference {
  wallets: {
    id: string;
    name: string;
  }[]
}

type WalletActions = "deposit" | "withdraw";

export const WalletsPage = () => {
  const [htmlContent, setHtmlContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [walletActionsModalVisible, setWalletActionsModalVisible] =
    useState<WalletActions | null>(null);
  const navigate = useNavigate();

  const fetchWallets = useCallback(() => {
    fetch(`${API_URL}/wallets/list`, {
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
          console.error("Failed to fetch wallets:", error);
        }
      });
  }, [navigate]);

  useEffect(() => {
    fetchWallets();
  }, [fetchWallets]);

  const createWallet = (values: WalletFormValues) => {
    fetch(`${API_URL}/wallets/item`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(values),
    })
      .then(() => {
        setOpen(false);
        fetchWallets();
      })
      .catch((error) => console.error(error));
  };

  const [walletOptions, setWalletOptions] = useState<{ label: string; value: string }[]>([]);

  const fetchWalletReferences = useCallback(() => {
    fetch(`${API_URL}/wallets/reference`, {
      method: "GET",
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data: WalletReference) => {
        const options = data.wallets.map(({ id, name }) => ({
          value: id,
          label: name,
        }));
        setWalletOptions(options);
      })
      .catch((error) => console.error("Failed to fetch wallet references", error));
  }, []);

  useEffect(() => {
    if (walletActionsModalVisible) {
      fetchWalletReferences();
    }
  }, [walletActionsModalVisible, fetchWalletReferences]);

  const performWalletAction = (values: WalletActionsFormValues) => {
    fetch(`${API_URL}/wallets/item/${values.walletId}/${values.type}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        amount: values.amount,
      }),
    })
      .then(() => {
        setWalletActionsModalVisible(null);
        fetchWallets();
      })
      .catch((error) => console.error("Failed to perform action", error));
  };

  if (loading) return <div>Loading wallets...</div>;

  return (
    <>
      <div className="wallets-container">
        <div
          className="transactions-buttons"
          style={{ display: "flex", flexDirection: "row", gap: "1rem" }}
        >
          <Button onClick={() => setOpen(true)}>New Wallet</Button>
          <Button onClick={() => setWalletActionsModalVisible("deposit")}>
            Deposit
          </Button>
          <Button onClick={() => setWalletActionsModalVisible("withdraw")}>
            Withdraw
          </Button>
        </div>
        <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
      </div>
      <Modal
        title="New Wallet"
        open={open}
        footer={null}
        onClose={() => setOpen(false)}
        onCancel={() => setOpen(false)}
      >
        <Form<WalletFormValues> layout="vertical" onFinish={createWallet}>
          <Form.Item<WalletFormValues>
            label="Wallet Name"
            name="name"
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item<WalletFormValues>
            label="Wallet Currency"
            name="currency"
            rules={[{ required: true }]}
          >
            <Select options={currencyOptions} />
          </Form.Item>

          <Form.Item label={null}>
            <Button type="primary" htmlType="submit">
              Create
            </Button>
          </Form.Item>
        </Form>
      </Modal>
      <Modal
        title={
          walletActionsModalVisible === "deposit"
            ? "Deposit to Wallet"
            : "Withdraw from Wallet"
        }
        open={walletActionsModalVisible !== null}
        onCancel={() => setWalletActionsModalVisible(null)}
        footer={null}
      >
        <Form<WalletActionsFormValues>
          layout="vertical"
          onFinish={(values) => {
            if (walletActionsModalVisible) {
              performWalletAction({ ...values, type: walletActionsModalVisible });
            }
          }}
        >
          <Form.Item name="walletId" label="Select Wallet" rules={[{ required: true }]}>
            <Select placeholder="Select a wallet" options={walletOptions} />
          </Form.Item>
          <Form.Item name="amount">
            <InputNumber placeholder="Amount" />
          </Form.Item>
          <div style={{ display: "flex", flexDirection: "row", gap: "1rem" }}>
            <Button onClick={() => setWalletActionsModalVisible(null)}>
              Close
            </Button>
            <Form.Item label={null}>
              <Button type="primary" htmlType="submit">
                {walletActionsModalVisible === "deposit" ? "Deposit" : "Withdraw"}
              </Button>
            </Form.Item>
          </div>
        </Form>
      </Modal>
    </>
  );
};
