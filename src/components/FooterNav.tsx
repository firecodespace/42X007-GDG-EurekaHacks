"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const items = [
    { href: "/", label: "Home" },
    { href: "/explore", label: "Explore" },
    { href: "/profile", label: "Profile" },
    { href: "/onboarding", label: "Sign up" },
];

export default function FooterNav() {
    const pathname = usePathname();

    return (
        <footer className="w-full border-t border-white/10 bg-black/20 backdrop-blur-xl">
            <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 text-sm">
                <div className="text-white/50">HackFlix</div>

                <nav className="flex items-center gap-6">
                    {items.map((it) => {
                        const active = pathname === it.href || pathname.startsWith(it.href + "/");
                        return (
                            <Link
                                key={it.href}
                                href={it.href}
                                className={active ? "text-white" : "text-white/60 hover:text-white/90"}
                            >
                                {it.label}
                            </Link>
                        );
                    })}
                </nav>
            </div>
        </footer>
    );
}
