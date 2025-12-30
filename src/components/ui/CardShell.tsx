import type { PropsWithChildren } from "react";
import clsx from "clsx";

type CardShellProps = PropsWithChildren<{
    className?: string;
}>;

export function CardShell({ className, children }: CardShellProps) {
    return (
        <section
            className={clsx(
                "relative w-full select-none",
                "h-[420px] max-w-[400px]",
                "rounded-none",
                "bg-[linear-gradient(135deg,_#002480_7%,_#000D2E_36%)]",
                "shadow-[5px_5px_11px_0px_#75FFEB]",
                className
            )}
        >
            <div className="h-full w-full p-[15px]">{children}</div>
        </section>
    );
}
