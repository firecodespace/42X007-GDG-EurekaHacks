// src/app/profile/layout.tsx
import ProfileSidebar from "./_components/ProfileSidebar";

export default function ProfileLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-dvh text-white">
            {/* background is your existing static background layer */}
            <div className="pointer-events-none fixed inset-0 -z-10">
                {/* keep your background component/div here */}
            </div>

            <div className="mx-auto max-w-[1800px] px-6 lg:px-8">
                <div className="pt-[120px] grid grid-cols-1 lg:grid-cols-12 gap-8">
                    {/* Left: fixed/sticky - 25% width */}
                    <aside className="hidden lg:block lg:col-span-3">
                        <div className="sticky top-[120px]">
                            <ProfileSidebar />
                        </div>
                    </aside>

                    {/* Right: static background panel, inner scroll only */}
                    <section className="col-span-1 lg:col-span-9">
                        {/* Outer panel: touches bottom, no bottom curves */}
                        <div className="h-[calc(100dvh-160px)] border border-white/10 bg-white/5 backdrop-blur-xl shadow-[0_0_0_1px_rgba(255,255,255,0.05)] rounded-t-3xl rounded-b-none">
                            {/* Inner: scrollable content */}
                            <div className="h-full overflow-auto p-8 sm:p-10 lg:p-12">
                                {children}
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </div>
    );
}
