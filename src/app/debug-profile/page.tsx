// src/app/debug-profile/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useAuthUser } from "@/lib/auth/useAuthUser";
import { fetchUserJson } from "@/lib/profile/fetchUserJson";

export default function DebugProfilePage() {
    const { user } = useAuthUser();
    const [json, setJson] = useState(null);
    const [loading, setLoading] = useState(false);

    const fetchData = async () => {
        if (!user?.uid) return;
        setLoading(true);
        try {
            const data = await fetchUserJson(user.uid);
            setJson(data);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, [user?.uid]);

    if (!user) {
        return <div className="p-8 text-white">Sign in first</div>;
    }

    return (
        <div className="p-8 max-w-4xl mx-auto text-white">
            <h1 className="text-2xl font-bold mb-4">Debug Profile</h1>
            <p>User UID: <code className="bg-black/20 px-2 py-1 rounded">{user.uid}</code></p>

            <button
                onClick={fetchData}
                className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded text-white"
            >
                {loading ? "Loading..." : "Refresh"}
            </button>

            {json && (
                <>
                    <h2 className="text-xl mt-8 mb-4">Full JSON:</h2>
                    <pre className="bg-black/50 p-6 rounded-xl overflow-auto text-xs">
                        {JSON.stringify(json, null, 2)}
                    </pre>
                </>
            )}
        </div>
    );
}
