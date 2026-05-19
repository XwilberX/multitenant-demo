import { useEffect, useState } from 'react'

export default function App() {
  const [me, setMe] = useState(null)
  const [branding, setBranding] = useState(null)
  const [features, setFeatures] = useState({})
  const [products, setProducts] = useState([])
  const [orders, setOrders] = useState([])
  const [receipt, setReceipt] = useState(null)

  useEffect(() => {
    Promise.all([
      fetch('/api/me').then(r => r.json()),
      fetch('/api/branding').then(r => r.json()),
      fetch('/api/features').then(r => r.json()),
      fetch('/api/products').then(r => r.json()),
      fetch('/api/orders').then(r => r.json()),
    ]).then(([me, branding, features, products, orders]) => {
      setMe(me)
      setBranding(branding)
      setFeatures(features)
      setProducts(products)
      setOrders(orders)
      document.documentElement.style.setProperty('--primary-color', branding.color)
      document.title = `${branding.name} — Multitenant Demo`
    })
  }, [])

  async function checkout(productId) {
    const res = await fetch('/api/checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: productId }),
    })
    const data = await res.json()
    setReceipt(data)
  }

  if (!branding) return <div style={{ padding: '2rem' }}>Cargando…</div>

  return (
    <>
      <header>
        <div className="logo">{branding.logo_text}</div>
        <div>{branding.name}</div>
        <div className="tenant-pill">tenant: {me?.slug}</div>
      </header>
      <main>
        <section className="card">
          <h2>Catálogo de productos</h2>
          {products.map(p => (
            <div className="product" key={p.id}>
              <div>{p.name}</div>
              <div>
                <span className="product-price">${p.price.toFixed(2)} MXN</span>
                <button onClick={() => checkout(p.id)}>Comprar</button>
              </div>
            </div>
          ))}
          {receipt && (
            <pre className="receipt">{JSON.stringify(receipt, null, 2)}</pre>
          )}
        </section>

        <section className="card">
          <h2>Órdenes recientes</h2>
          {orders.map(o => (
            <div className="product" key={o.id}>
              <div>
                {o.product}
                <span className={`badge ${o.status}`}>{o.status}</span>
              </div>
              <div className="product-price">${o.amount.toFixed(2)}</div>
            </div>
          ))}
        </section>

        {features.enable_advanced_dashboard && (
          <section className="card dashboard-card">
            <h2>Dashboard avanzado</h2>
            <p style={{ opacity: 0.85, marginTop: 0 }}>
              Métricas exclusivas para tenants con plan avanzado.
            </p>
            <div className="metric">
              <strong>$45,231</strong>
              <span>Ventas del mes</span>
            </div>
            <div className="metric">
              <strong>127</strong>
              <span>Órdenes</span>
            </div>
            <div className="metric">
              <strong>98.2%</strong>
              <span>Conversión</span>
            </div>
          </section>
        )}
      </main>
    </>
  )
}
