// src/app/profile/_components/InterestsSection.tsx
"use client";

import { useState } from "react";
import { X } from "lucide-react";
import { UserProfile } from "@/lib/profile/useProfile";
import { updateProfileField } from "@/lib/profile/updateProfile";

type Props = {
    profile: UserProfile;
};

export default function InterestsSection({ profile }: Props) {
    const [interests, setInterests] = useState<string[]>(profile.interests);
    const [domains, setDomains] = useState<string[]>(profile.preferred_domains);
    const [interestInput, setInterestInput] = useState("");
    const [domainInput, setDomainInput] = useState("");
    const [saving, setSaving] = useState(false);

    const handleAddInterest = async () => {
        if (!interestInput.trim()) return;
        const newInterests = [...interests, interestInput.trim()];
        setInterests(newInterests);
        setInterestInput("");

        setSaving(true);
        try {
            await updateProfileField(profile.uid, "interests", newInterests);
        } finally {
            setSaving(false);
        }
    };

    const handleRemoveInterest = async (index: number) => {
        const newInterests = interests.filter((_, i) => i !== index);
        setInterests(newInterests);

        setSaving(true);
        try {
            await updateProfileField(profile.uid, "interests", newInterests);
        } finally {
            setSaving(false);
        }
    };

    const handleAddDomain = async () => {
        if (!domainInput.trim()) return;
        const newDomains = [...domains, domainInput.trim()];
        setDomains(newDomains);
        setDomainInput("");

        setSaving(true);
        try {
            await updateProfileField(profile.uid, "preferred_domains", newDomains);
        } finally {
            setSaving(false);
        }
    };

    const handleRemoveDomain = async (index: number) => {
        const newDomains = domains.filter((_, i) => i !== index);
        setDomains(newDomains);

        setSaving(true);
        try {
            await updateProfileField(profile.uid, "preferred_domains", newDomains);
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="space-y-6">
            {/* Interests */}
            <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <h2 className="text-xl font-semibold mb-4">Interests</h2>

                <div className="flex gap-3 mb-6">
                    <input
                        type="text"
                        value={interestInput}
                        onChange={(e) => setInterestInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleAddInterest()}
                        placeholder="Add an interest (e.g. AI/ML, Web3)"
                        className="flex-1 h-12 px-4 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:border-white/30"
                        disabled={saving}
                    />
                    <button
                        onClick={handleAddInterest}
                        disabled={saving || !interestInput.trim()}
                        className="px-6 h-12 rounded-xl bg-white text-black font-medium disabled:opacity-50"
                    >
                        Add
                    </button>
                </div>

                <div className="flex flex-wrap gap-2">
                    {interests.map((interest, i) => (
                        <div
                            key={i}
                            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 border border-white/20 text-white"
                        >
                            <span>{interest}</span>
                            <button
                                onClick={() => handleRemoveInterest(i)}
                                disabled={saving}
                                className="hover:bg-white/20 rounded-full p-0.5"
                            >
                                <X className="h-4 w-4" />
                            </button>
                        </div>
                    ))}
                    {interests.length === 0 && (
                        <p className="text-white/40 text-sm">No interests added yet</p>
                    )}
                </div>
            </div>

            {/* Preferred Domains */}
            <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                <h2 className="text-xl font-semibold mb-4">Preferred Domains</h2>

                <div className="flex gap-3 mb-6">
                    <input
                        type="text"
                        value={domainInput}
                        onChange={(e) => setDomainInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleAddDomain()}
                        placeholder="Add a domain (e.g. Full Stack, DevOps)"
                        className="flex-1 h-12 px-4 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:border-white/30"
                        disabled={saving}
                    />
                    <button
                        onClick={handleAddDomain}
                        disabled={saving || !domainInput.trim()}
                        className="px-6 h-12 rounded-xl bg-white text-black font-medium disabled:opacity-50"
                    >
                        Add
                    </button>
                </div>

                <div className="flex flex-wrap gap-2">
                    {domains.map((domain, i) => (
                        <div
                            key={i}
                            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 border border-white/20 text-white"
                        >
                            <span>{domain}</span>
                            <button
                                onClick={() => handleRemoveDomain(i)}
                                disabled={saving}
                                className="hover:bg-white/20 rounded-full p-0.5"
                            >
                                <X className="h-4 w-4" />
                            </button>
                        </div>
                    ))}
                    {domains.length === 0 && (
                        <p className="text-white/40 text-sm">No domains added yet</p>
                    )}
                </div>
            </div>
        </div>
    );
}
