import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const Registr = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState({});
  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      const response = await fetch("http://127.0.0.1:8000/api/registr", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });
      if (response.ok) {
        const data = await response.json();
        navigate("/login");
      } else {
        const data = await response.json();
        setError(data);
        console.log(data);
      }
    } catch (e) {
    } finally {
      setLoading(false);
    }
  };

  return (
    <form method="post" onSubmit={handleSubmit}>
      <input
        type="email"
        required
        placeholder="email"
        value={form.email}
        name="email"
        onChange={(e) => setForm({ ...form, [e.target.name]: e.target.value })}
      />
      {error.email && <p className="text-red-800">{error.email}</p>}
      <input
        type="password"
        required
        placeholder="password"
        value={form.password}
        name="password"
        onChange={(e) => setForm({ ...form, [e.target.name]: e.target.value })}
      />
      <button disabled={loading}>Отправить</button>
    </form>
  );
};
