import { createBrowserRouter, RouterProvider, NavLink, Outlet } from 'react-router-dom'
import { Home } from '@/pages/Home'
import { Results } from '@/pages/Results'
import { Populations } from '@/pages/Populations'
import { History } from '@/pages/History'

function Layout() {
  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `text-sm font-medium transition-colors hover:text-primary ${
      isActive ? 'text-primary' : 'text-muted-foreground'
    }`

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b sticky top-0 z-10 bg-background/95 backdrop-blur">
        <div className="max-w-3xl mx-auto px-4 h-14 flex items-center justify-between">
          <NavLink to="/" className="font-bold text-lg">
            ✨ Country Simulator
          </NavLink>
          <nav className="flex gap-6">
            <NavLink to="/" className={linkClass} end>
              Home
            </NavLink>
            <NavLink to="/populations" className={linkClass}>
              Populations
            </NavLink>
            <NavLink to="/history" className={linkClass}>
              History
            </NavLink>
          </nav>
        </div>
      </header>
      <main className="max-w-3xl mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'results/:runId', element: <Results /> },
      { path: 'populations', element: <Populations /> },
      { path: 'history', element: <History /> },
    ],
  },
])

export default function App() {
  return <RouterProvider router={router} />
}
