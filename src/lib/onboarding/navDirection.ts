// src/lib/onboarding/navDirection.ts
"use client";

import { usePathname } from "next/navigation";
import { useEffect } from "react";

export function useNavDirection() {
    const pathname = usePathname();

    const forward = () => {
        // Remove onboarding prefix and go to next logical step
        const step = pathname.replace("/onboarding/", "");
        // Your existing nav logic here
        console.log("Navigating forward from:", step);
    };

    return { forward };
}
