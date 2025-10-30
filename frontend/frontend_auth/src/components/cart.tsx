import React, { useEffect, useState } from "react";
import { FaPlus, FaMinus, FaTrash } from "react-icons/fa";

interface CartItem {
  product_id: string;
  name: string;
  price: number;
  quantity: number;
}

const Cart: React.FC = () => {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const username = localStorage.getItem("username");
  const token = localStorage.getItem("authToken");
  const API_URL = "http://localhost:8000/api/v1/cart";

  // 🟢 Fetch Cart
  useEffect(() => {
    const fetchCart = async () => {
      if (!username || !token) return;
      try {
        setLoading(true);
        const res = await fetch(`${API_URL}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!res.ok) throw new Error(`Failed to fetch cart (${res.status})`);
        const data = await res.json();

        console.log("Cart API Response:", data);

        // ✅ normalize structure
        if (Array.isArray(data)) {
          setCartItems(data);
        } else if (Array.isArray(data.items)) {
          setCartItems(data.items);
        } else if (data.cart && Array.isArray(data.cart.items)) {
          setCartItems(data.cart.items);
        } else {
          setCartItems([]);
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCart();
  }, [username, token]);

  // 🧮 Calculate total safely
  const total = Array.isArray(cartItems)
    ? cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0)
    : 0;

  // ➕ Increase quantity
  const increaseQuantity = async (productId: string) => {
    const updated = cartItems.map((i) =>
      i.product_id === productId ? { ...i, quantity: i.quantity + 1 } : i
    );
    setCartItems(updated);

    await fetch(`${API_URL}/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        username,
        product: { product_id: productId, quantity: 1 },
      }),
    });
  };

  // ➖ Decrease quantity
  const decreaseQuantity = async (productId: string) => {
    const item = cartItems.find((i) => i.product_id === productId);
    if (!item) return;

    if (item.quantity <= 1) return removeItem(productId);

    const updated = cartItems.map((i) =>
      i.product_id === productId
        ? { ...i, quantity: i.quantity - 1 }
        : i
    );
    setCartItems(updated);

    await fetch(`${API_URL}/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        username,
        product: { product_id: productId, quantity: -1 },
      }),
    });
  };

  // 🗑️ Remove item
  const removeItem = async (productId: string) => {
    const updated = cartItems.filter((i) => i.product_id !== productId);
    setCartItems(updated);

    await fetch(`${API_URL}/remove/${productId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
  };

  // 🧹 Clear all
  const clearCart = async () => {
    await fetch(`${API_URL}/clear`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    setCartItems([]);
  };

  if (loading)
    return <p className="p-8 text-gray-400 text-center">Loading cart...</p>;
  if (error)
    return <p className="p-8 text-red-500 text-center">{error}</p>;

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center py-8 px-4">
      <h1 className="text-3xl font-bold mb-6 flex items-center gap-2">
        🛒 Your Cart
      </h1>

      {cartItems.length === 0 ? (
        <p className="text-gray-400 text-lg mt-10">Your cart is empty.</p>
      ) : (
        <div className="w-full max-w-3xl space-y-4">
          {cartItems.map((item) => (
            <div
              key={item.product_id}
              className="flex justify-between items-center border border-gray-700 rounded-lg p-4 bg-black shadow-sm hover:shadow-md hover:border-gray-500 transition-all duration-200"
            >
              <div>
                <h2 className="text-lg font-semibold">{item.name}</h2>
                <p className="text-gray-400">
                  ₹{item.price} × {item.quantity}
                </p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => decreaseQuantity(item.product_id)}
                  className="bg-yellow-500 hover:bg-yellow-400 text-black rounded px-2 py-1"
                >
                  <FaMinus />
                </button>
                <button
                  onClick={() => increaseQuantity(item.product_id)}
                  className="bg-green-500 hover:bg-green-400 text-black rounded px-2 py-1"
                >
                  <FaPlus />
                </button>
                <button
                  onClick={() => removeItem(item.product_id)}
                  className="bg-red-600 hover:bg-red-500 text-white rounded px-2 py-1"
                >
                  <FaTrash />
                </button>
              </div>
            </div>
          ))}

          <div className="flex justify-between items-center mt-8">
            <button
              onClick={clearCart}
              className="bg-red-700 hover:bg-red-600 text-white px-4 py-2 rounded-md"
            >
              Clear Cart
            </button>
            <h3 className="text-xl font-semibold">
              Total: ₹{total.toLocaleString()}
            </h3>
          </div>
        </div>
      )}
    </div>
  );
};

export default Cart;
