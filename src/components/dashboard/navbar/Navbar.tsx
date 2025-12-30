"use client";

import Link from "next/link";
import { useEffect, useId, useRef, useState } from "react";
import { NAV_LINKS } from "./nav-links";
import { Button } from "@/components/ui/Button";
import { CONTENT_INSET_CLASS } from "@/components/ui/layout";

function CloseIcon() {
    return (
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="2" />
        </svg>
    );
}

export function Navbar() {
    const [open, setOpen] = useState(false);
    const dialogId = useId();
    const panelRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        function onKeyDown(e: KeyboardEvent) {
            if (e.key === "Escape") setOpen(false);
        }
        if (open) document.addEventListener("keydown", onKeyDown);
        return () => document.removeEventListener("keydown", onKeyDown);
    }, [open]);

    useEffect(() => {
        if (open) panelRef.current?.focus();
    }, [open]);

    return (
        <>
            <header className="sticky top-0 z-40">
                <nav className="w-full bg-transparent backdrop-blur-[6px]">
                    <div
                        className={[
                            "mx-auto flex w-full items-center justify-between",
                            CONTENT_INSET_CLASS, // 56px L/R alignment with rails
                            "py-3", // smaller height
                        ].join(" ")}
                    >
                        <Link href="/" className="text-3xl font-semibold tracking-tight text-white">
                            HackFlix
                        </Link>

                        {/* Desktop nav */}
                        <div className="hidden items-center gap-10 lg:flex">
                            <div className="flex items-center gap-10">
                                {NAV_LINKS.map((l) => (
                                    <Link
                                        key={l.href}
                                        href={l.href}
                                        className="text-lg text-white/80 hover:text-white"
                                    >
                                        {l.label}
                                    </Link>
                                ))}
                            </div>

                            <Button href="/signup" className="min-w-[160px]">
                                sign up
                            </Button>
                        </div>

                        {/* Mobile hamburger */}
                        <button
                            type="button"
                            className="inline-flex h-[45px] items-center justify-center rounded-none px-3 text-white/90 hover:text-white lg:hidden"
                            aria-label="Open menu"
                            aria-controls={dialogId}
                            aria-expanded={open}
                            onClick={() => setOpen(true)}
                        >
                            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                                <path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" strokeWidth="2" />
                            </svg>
                        </button>
                    </div>
                </nav>
            </header>

            {/* Mobile overlay + drawer */}
            {open ? (
                <div id={dialogId} role="dialog" aria-modal="true" className="fixed inset-0 z-50 lg:hidden">
                    {/* Optional dark wash to match your theme */}
                    <div className="absolute inset-0 z-0 bg-[#000D2E]/35" />

                    {/* Click outside to close */}
                    <button
                        aria-label="Close menu"
                        className="absolute inset-0 z-10 bg-transparent"
                        onClick={() => setOpen(false)}
                    />

                    {/* Drawer panel */}
                    <div
                        ref={panelRef}
                        tabIndex={-1}
                        className={[
                            "absolute right-0 top-0 z-20 h-full w-[min(360px,90vw)]",
                            "bg-[#000D2E]",
                            "shadow-[0_0_0_1px_rgba(255,255,255,0.12)]",
                            "outline-none",
                            "px-6 py-6",
                        ].join(" ")}
                    >
                        <div className="flex items-center justify-between">
                            <span className="text-lg font-semibold text-white">HackFlix</span>
                            <button
                                type="button"
                                className="h-[45px] px-2 text-white/80 hover:text-white"
                                aria-label="Close"
                                onClick={() => setOpen(false)}
                            >
                                <CloseIcon />
                            </button>
                        </div>

                        <nav className="mt-8 flex flex-col gap-5">
                            {/* Optional extra top item */}
                            <Link
                                href="#"
                                onClick={() => setOpen(false)}
                                className="text-base text-white/85 hover:text-white"
                            >
                                See recommendations
                            </Link>

                            {NAV_LINKS.map((l) => (
                                <Link
                                    key={l.href}
                                    href={l.href}
                                    onClick={() => setOpen(false)}
                                    className="text-base text-white/85 hover:text-white"
                                >
                                    {l.label}
                                </Link>
                            ))}
                        </nav>

                        <div className="mt-10">
                            <Button href="/onboarding" className="w-full">
                                sign up
                            </Button>
                        </div>
                    </div>
                </div>
            ) : null}
        </>
    );
}
