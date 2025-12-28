export default function ProfilePage() {
    return (
        <main className="min-h-dvh px-10 py-16 text-white">
            <div className="max-w-3xl">
                <h1 className="text-4xl font-semibold">Your Profile</h1>
                <p className="mt-3 text-white/70">
                    Profile editing will be connected to Firebase after the backend team finishes auth + storage.
                </p>

                <div className="mt-10 rounded-2xl border border-white/15 bg-black/20 backdrop-blur-md p-6">
                    <div className="text-white/60 text-sm">Sample profile card</div>
                    <div className="mt-4 space-y-2">
                        <Row k="Name" v="(from onboarding)" />
                        <Row k="Email" v="(from onboarding)" />
                        <Row k="University" v="(from onboarding)" />
                        <Row k="Course" v="(from onboarding)" />
                    </div>

                    <button
                        type="button"
                        className="mt-6 rounded-xl border border-white/20 px-5 py-3 text-white"
                    >
                        Edit
                    </button>
                </div>
            </div>
        </main>
    );
}

function Row({ k, v }: { k: string; v: string }) {
    return (
        <div className="flex items-center justify-between gap-6">
            <div className="text-white/70">{k}</div>
            <div className="text-white">{v}</div>
        </div>
    );
}
