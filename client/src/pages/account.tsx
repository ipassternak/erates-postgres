import { useEffect, useState } from "react";
import { API_URL } from "../const";
import { useNavigate } from "react-router-dom";

type ErrorResponse = {
  detail: string;
};

type UserData = {
  item: {
    full_name: string;
    email: string;
    role: string;
  };
};

type ApiResponse = UserData | ErrorResponse;

export const AccountPage = () => {
  const [apiResponse, setApiResponse] = useState<ApiResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    setIsLoading(true);
    fetch(`${API_URL}/auth/me`, {
      method: "GET",
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => setApiResponse(data))
      .catch((error) => console.error(error))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) return <div>Loading...</div>;

  const isErrorResponse = (
    response: ApiResponse | null
  ): response is ErrorResponse => {
    return !!response && "detail" in response;
  };

  const isError = isErrorResponse(apiResponse);

  if (!apiResponse || isError) {
    return (
      <div>
        <h1>You are not logged in</h1>
        <button onClick={() => navigate("/login")}>Login</button>
        <button onClick={() => navigate("/register")}>Register</button>
      </div>
    );
  }

  return (
    <div className="account-page">
      <h1>Name: {apiResponse.item.full_name}</h1>
      <p>Email: {apiResponse.item.email}</p>
      <p>Role: {apiResponse.item.role}</p>
    </div>
  );
};
