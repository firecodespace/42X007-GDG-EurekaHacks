import { OnboardingProvider } from "@/lib/onboarding/store";
import OnboardingTransition from "@/app/onboarding/_components/OnboardingTransition";

export default function OnboardingLayout({ children }: { children: React.ReactNode }) {
    return (
        <OnboardingProvider>
            <OnboardingTransition>{children}</OnboardingTransition>
        </OnboardingProvider>
    );
}
