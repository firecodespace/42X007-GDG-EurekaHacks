export default function SectionHeader({
    title,
    subtitle,
}: {
    title: string;
    subtitle?: string;
}) {
    return (
        <div className="mb-8">
            <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight">{title}</h1>
            {subtitle ? <p className="mt-2 text-white/60">{subtitle}</p> : null}
        </div>
    );
}
