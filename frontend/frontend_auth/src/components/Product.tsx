import { useState, useEffect } from "react";

interface Product {
  product_id: string;
  name: string;
  category: string;
  price: number;
  image: string;
}

export default function ProductList() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("authToken");
  const API_URL = "http://localhost:8000/api/v1";

  useEffect(() => {
    fetch(`${API_URL}/products`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then(setProducts)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const addToCart = async (product: Product) => {
    await fetch(`${API_URL}/cart/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        product_id: product.product_id,
        name: product.name,
        price: product.price,
        quantity: 1,
      }),
    });
  };

  if (loading) return <p className="text-center mt-20 text-gray-400">Loading...</p>;

  return (
    <div className="min-h-screen bg-black text-white px-6 py-10">
      <h2 className="text-3xl font-bold text-center mb-8 text-gray-100">
        ✨ Featured Products
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {products.map((product) => (
          <div
            key={product.product_id}
            className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 shadow-lg hover:scale-105 transition-transform duration-300"
          >
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-40 object-cover rounded-lg mb-4"
            />
            <h3 className="text-lg font-semibold text-white">{product.name}</h3>
            <p className="text-sm text-gray-400">{product.category}</p>
            <p className="text-lg font-bold text-green-400 mt-2">
              ₹{product.price.toLocaleString()}
            </p>
            <button
              onClick={() => addToCart(product)}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg mt-4 transition"
            >
              ➕ Add to Cart
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
