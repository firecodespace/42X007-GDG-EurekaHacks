"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

type Props = {
    href: string;
    icon?: React.ReactNode;
    label: string;
};

export default function ProfileNavItem({ href, icon, label }: Props) {
    const pathname = usePathname();
    const active = pathname === href || pathname.startsWith(href + "/");

    return (
        <Link
            href={href}
            className={[
                "flex items-center gap-3 rounded-2xl px-4 py-3 transition",
                active ? "bg-white/10 text-white" : "text-white/80 hover:bg-white/5 hover:text-white",
            ].join(" ")}
        >
            <span className="opacity-90">{icon}</span>
            <span className="text-base">{label}</span>
        </Link>
    );
}
