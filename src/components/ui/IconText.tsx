import type { ReactNode } from "react";

type IconTextProps = {
    icon: ReactNode;
    text: string;
    className?: string;
};

export function IconText({ icon, text, className }: IconTextProps) {
    return (
        <div className={`flex items-center gap-2 text-white/80 ${className ?? ""}`}>
            <span className="text-white/70">{icon}</span>
            <span className="text-sm leading-none">{text}</span>
        </div>
    );
}
