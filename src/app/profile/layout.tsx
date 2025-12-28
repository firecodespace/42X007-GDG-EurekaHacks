import ProfileSidebar from "./_components/ProfileSidebar";

export default function ProfileLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-dvh text-white">
            {/* background is your existing static background layer */}
            <div className="pointer-events-none fixed inset-0 -z-10">
                {/* keep your background component/div here */}
            </div>

            <div className="mx-auto max-w-7xl px-6">
                <div className="pt-[120px] grid grid-cols-12 gap-8">
                    {/* Left: fixed/sticky */}
                    <aside className="col-span-3">
                        <div className="sticky top-[120px]">
                            <ProfileSidebar />
                        </div>
                    </aside>

                    {/* Right: independently scrollable floating panel */}
                    <section className="col-span-9">
                        <div className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl shadow-[0_0_0_1px_rgba(255,255,255,0.05)]">
                            <div className="max-h-[calc(100dvh-160px)] overflow-auto p-10">
                                {children}
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </div>
    );
}
