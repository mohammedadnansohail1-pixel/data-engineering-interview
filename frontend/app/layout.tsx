import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Data Engineering Interview Prep',
  description: 'AI-powered interview preparation platform for data engineers',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
