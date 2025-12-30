import type { Metadata } from "next";
import "./globals.css";
import AppBackground from "@/components/layout/AppBackground";
import { Space_Grotesk } from "next/font/google";
import FooterNav from "@/components/FooterNav";


const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Hackflix",
  description: "Discover hackathons and events.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${spaceGrotesk.className} min-h-dvh`}>
        <AppBackground />
        <div className="relative z-10 min-h-dvh">{children}</div>
        <FooterNav />
      </body>
    </html>
  );
}
