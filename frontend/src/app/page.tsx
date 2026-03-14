import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen">
      <header className="border-b">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-primary">Reroute</h1>
          <nav className="flex gap-6">
            <Link href="/calculator" className="hover:text-primary transition">
              Compensation Calculator
            </Link>
            <Link href="/dashboard" className="hover:text-primary transition">
              Dashboard
            </Link>
            <Link
              href="/login"
              className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition"
            >
              Sign In
            </Link>
          </nav>
        </div>
      </header>

      <main>
        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-5xl font-bold mb-6 leading-tight">
              The first travel agent that acts <span className="text-primary">before</span> the bags stop moving
            </h2>
            <p className="text-xl text-secondary mb-8">
              Auto-rebooks flights and files compensation claims the moment disruption hits.
              Turn flight disruption from a crisis into a handled event.
            </p>
            <div className="flex justify-center gap-4">
              <Link
                href="/calculator"
                className="px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-dark transition text-lg"
              >
                Free Compensation Calculator
              </Link>
              <Link
                href="/signup"
                className="px-6 py-3 border border-primary text-primary rounded-lg hover:bg-primary/10 transition text-lg"
              >
                Get Started
              </Link>
            </div>
          </div>
        </section>

        <section className="py-16 px-4 bg-card">
          <div className="max-w-6xl mx-auto">
            <h3 className="text-3xl font-bold text-center mb-12">How It Works</h3>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center p-6">
                <div className="text-4xl mb-4">📡</div>
                <h4 className="text-xl font-semibold mb-2">Monitor</h4>
                <p className="text-secondary">
                  We track your flights in real-time using public airline data feeds
                </p>
              </div>
              <div className="text-center p-6">
                <div className="text-4xl mb-4">🔄</div>
                <h4 className="text-xl font-semibold mb-2">Rebook</h4>
                <p className="text-secondary">
                  Instant rebooking based on your stored preferences (seat, loyalty, connections)
                </p>
              </div>
              <div className="text-center p-6">
                <div className="text-4xl mb-4">💰</div>
                <h4 className="text-xl font-semibold mb-2">Claim</h4>
                <p className="text-secondary">
                  Automatic compensation filing for EU flights under EC 261/2004
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="py-16 px-4">
          <div className="max-w-4xl mx-auto">
            <h3 className="text-3xl font-bold text-center mb-12">Pricing</h3>
            <div className="grid md:grid-cols-2 gap-8 max-w-3xl mx-auto">
              <div className="border rounded-xl p-8">
                <h4 className="text-2xl font-bold mb-2">Basic</h4>
                <p className="text-4xl font-bold text-primary mb-4">$29<span className="text-lg text-secondary">/month</span></p>
                <ul className="space-y-3 text-secondary">
                  <li>✓ Real-time flight monitoring</li>
                  <li>✓ Instant disruption alerts</li>
                  <li>✓ Email & push notifications</li>
                </ul>
              </div>
              <div className="border-2 border-primary rounded-xl p-8 relative">
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-white px-4 py-1 rounded-full text-sm">
                  Most Popular
                </div>
                <h4 className="text-2xl font-bold mb-2">Core</h4>
                <p className="text-4xl font-bold text-primary mb-4">$29<span className="text-lg text-secondary">/mo</span> + 25%</p>
                <p className="text-sm text-secondary mb-4">25% of successful claims</p>
                <ul className="space-y-3 text-secondary">
                  <li>✓ Everything in Basic</li>
                  <li>✓ Automatic rebooking</li>
                  <li>✓ Claims filing & tracking</li>
                  <li>✓ ML-powered success prediction</li>
                </ul>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t py-8 px-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center text-secondary text-sm">
          <p>© 2026 Reroute. All rights reserved.</p>
          <div className="flex gap-4">
            <Link href="/privacy" className="hover:text-foreground">Privacy</Link>
            <Link href="/terms" className="hover:text-foreground">Terms</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
