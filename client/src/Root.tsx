import { useState, useEffect } from "react";
import { Outlet } from "react-router-dom";
import { NextUIProvider } from "@nextui-org/react";
import { ThemeProvider as NextThemesProvider, useTheme } from "next-themes";
import { ConfigProvider, theme as themeAntd } from "antd";
import NavbarPage from "./components/bar/Navbar";

function AppLayout() {
  const { theme } = useTheme();

  return (
    <ConfigProvider
      theme={{
        algorithm: theme === "light" ? themeAntd.defaultAlgorithm : themeAntd.darkAlgorithm,
      }}
    >
      <NavbarPage />
      <main className="Root container mx-auto">
        <Outlet />
      </main>
    </ConfigProvider>
  );
}

export default function Root() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <NextUIProvider>
      <NextThemesProvider attribute="class">
        <AppLayout />
      </NextThemesProvider>
    </NextUIProvider>
  );
}
