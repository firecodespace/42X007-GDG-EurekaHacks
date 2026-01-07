// src/app/profile/_components/ProfileNavItem.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";

type Props = {
    href: string;
    icon: ReactNode;
    label: string;
};

export default function ProfileNavItem({ href, icon, label }: Props) {
    const pathname = usePathname();
    const isActive = pathname === href;

    return (
        <Link
            href={href}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${isActive
                    ? "bg-white/20 text-white"
                    : "text-white/70 hover:bg-white/10 hover:text-white"
                }`}
        >
            {icon}
            <span className="font-medium">{label}</span>
        </Link>
    );
}
