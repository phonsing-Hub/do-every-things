import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Root from "./Root";
import Home from "./components/pages/Home";
import New from "./components/pages/New";
function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <Root />,
      children: [
        {
          path: "/",
          element: <Home />,
        },
        {
          path: "/new",
          element: <New/>
        }
      ],
    },
  ]);
  return <RouterProvider router={router} />;
}

export default App;
