"use client";

import EditableField from "./_components/EditableField";
import SectionHeader from "./_components/SectionHeader";
import { useState } from "react";

export default function ProfileAccountPage() {
    // Temporary local state; next step is to hydrate from Firestore.
    const [profile, setProfile] = useState({
        name: "—",
        email: "—",
        phone: "—",
        university: "—",
        course: "—",
        username: "—",
    });

    return (
        <div>
            <SectionHeader
                title="Account"
                subtitle="Manage your personal details. Changes are saved instantly."
            />

            <div className="rounded-2xl border border-white/10 bg-white/5">
                <div className="px-6">
                    <EditableField
                        label="Name"
                        value={profile.name}
                        onSave={async (next) => setProfile((p) => ({ ...p, name: next || "—" }))}
                    />
                    <EditableField
                        label="Email"
                        value={profile.email}
                        onSave={async (next) => setProfile((p) => ({ ...p, email: next || "—" }))}
                    />
                    <EditableField
                        label="Phone"
                        value={profile.phone}
                        onSave={async (next) => setProfile((p) => ({ ...p, phone: next || "—" }))}
                    />
                    <EditableField
                        label="University"
                        value={profile.university}
                        onSave={async (next) => setProfile((p) => ({ ...p, university: next || "—" }))}
                    />
                    <EditableField
                        label="Course"
                        value={profile.course}
                        onSave={async (next) => setProfile((p) => ({ ...p, course: next || "—" }))}
                    />
                    <EditableField
                        label="Username"
                        value={profile.username}
                        onSave={async (next) => setProfile((p) => ({ ...p, username: next || "—" }))}
                    />
                </div>
            </div>
        </div>
    );
}
