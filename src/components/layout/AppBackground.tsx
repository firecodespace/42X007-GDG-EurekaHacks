export default function AppBackground() {
    return (
        <div
            aria-hidden
            className="pointer-events-none fixed inset-0 z-0 overflow-hidden"
            style={{ backgroundColor: "#000D2E" }}
        >
            <div
                className="absolute left-[-25%] top-[120px] h-[180px] w-[150%] opacity-90 blur-[70px]"
                style={{
                    background:
                        "linear-gradient(90deg, rgba(111,0,255,0.8) 8%, rgba(99,255,188,0.88) 88%)",
                    transform: "rotate(6deg)",
                }}
            />
            <div
                className="absolute left-[-25%] top-[560px] h-[180px] w-[150%] opacity-90 blur-[70px]"
                style={{
                    background:
                        "linear-gradient(90deg, rgba(111,0,255,0.8) 8%, rgba(99,255,188,0.88) 88%)",
                    transform: "rotate(6deg)",
                }}
            />
        </div>
    );
}
