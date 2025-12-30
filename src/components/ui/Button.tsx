import Link from "next/link";
import clsx from "clsx";
import type { ReactNode } from "react";

type ButtonProps = {
    href: string;
    children: ReactNode;
    variant?: "primary" | "ghost";
    className?: string;
};

export function Button({
    href,
    children,
    variant = "primary",
    className,
}: ButtonProps) {
    const base = clsx(
        "inline-flex items-center justify-center",
        "transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#9AFFF7]/60",
        // No rounded corners anywhere.
        "rounded-none"
    );

    const styles =
        variant === "primary"
            ? clsx(
                "h-[45px] px-8 font-medium",
                "bg-[#9AFFF7] text-[#000D2E] hover:bg-[#86fff5]"
            )
            : clsx("h-[45px] px-0 text-white/80 hover:text-white");

    return (
        <Link href={href} className={clsx(base, styles, className)}>
            {children}
        </Link>
    );
}
