"use client";

import { ArrowLeft, ArrowRight } from "lucide-react";

export default function UnderlineStep(props: {
    label: string;
    value: string;
    onChange: (v: string) => void;

    canContinue: boolean;
    onContinue: () => void;

    onBack?: () => void;
    canBack?: boolean;

    disabled?: boolean;
    inputMode?: React.HTMLAttributes<HTMLInputElement>["inputMode"];
    type?: string;
}) {
    const isDisabled = Boolean(props.disabled);
    const canGoNext = props.canContinue && !isDisabled;
    const canGoBack = (props.canBack ?? true) && Boolean(props.onBack) && !isDisabled;

    return (
        <div className="w-full">
            <label className="block text-white/90 text-3xl">{props.label}</label>

            <div className="mt-10 flex items-end gap-4">
                <input
                    autoFocus
                    value={props.value}
                    onChange={(e) => props.onChange(e.target.value)}
                    inputMode={props.inputMode}
                    type={props.type ?? "text"}
                    onKeyDown={(e) => {
                        if (e.key !== "Enter") return;
                        e.preventDefault();
                        if (canGoNext) props.onContinue();
                    }}
                    className="w-full bg-transparent text-white text-4xl outline-none"
                />

                <div className="flex items-center gap-5">
                    <button
                        type="button"
                        aria-label="Back"
                        onClick={() => props.onBack?.()}
                        disabled={!canGoBack}
                        className="cursor-pointer text-white/80 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
                    >
                        <ArrowLeft className="h-6 w-6" />
                    </button>

                    <button
                        type="button"
                        aria-label="Continue"
                        onClick={props.onContinue}
                        disabled={!canGoNext}
                        className="cursor-pointer text-white/90 hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
                    >
                        <ArrowRight className="h-6 w-6" />
                    </button>
                </div>
            </div>

            <div className="mt-6 h-px w-full bg-white/30" />
        </div>
    );
}
