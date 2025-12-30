import clsx from "clsx";
import type { PropsWithChildren } from "react";

type PillProps = PropsWithChildren<{
    className?: string;
}>;

export function Pill({ className, children }: PillProps) {
    return (
        <span
            className={clsx(
                "inline-flex items-center gap-2 rounded-full px-3 py-1 text-sm",
                "border border-white/10 bg-white/5 text-white/90",
                className
            )}
        >
            {children}
        </span>
    );
}
