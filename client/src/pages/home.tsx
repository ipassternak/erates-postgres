import { useEffect, useState } from "react";
import { API_URL } from "../const";

export const HomePage = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [htmlPage, setHtmlPage] = useState("");

  useEffect(() => {
    setIsLoading(true);
    fetch(`${API_URL}/exchange-rate/list`, {
      method: "GET",
      credentials: "include",
    })
      .then((response) => response.text())
      .then((data) => setHtmlPage(data))
      .catch((error) => console.error(error))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return <div dangerouslySetInnerHTML={{ __html: htmlPage }} />;
};
