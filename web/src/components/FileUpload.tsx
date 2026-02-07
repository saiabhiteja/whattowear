import { useCallback, useState } from "react";
import { Upload, Image as ImageIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  accept?: string;
  label?: string;
  sublabel?: string;
  preview?: string | null;
  className?: string;
  compact?: boolean;
}

export default function FileUpload({
  onFileSelect,
  accept = "image/*",
  label = "Drop your image here or click to browse",
  sublabel = "PNG, JPG up to 10MB",
  preview,
  className,
  compact = false,
}: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [localPreview, setLocalPreview] = useState<string | null>(null);

  const displayPreview = preview || localPreview;

  const handleFile = useCallback(
    (file: File) => {
      onFileSelect(file);
      const reader = new FileReader();
      reader.onloadend = () => setLocalPreview(reader.result as string);
      reader.readAsDataURL(file);
    },
    [onFileSelect]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  return (
    <label
      className={cn(
        "relative flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed transition-all duration-200",
        isDragging
          ? "border-primary bg-primary/5 scale-[1.01]"
          : "border-border hover:border-primary/40 hover:bg-muted/50",
        compact ? "gap-2 p-4" : "gap-3 p-8",
        className
      )}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
    >
      {displayPreview ? (
        <img
          src={displayPreview}
          alt="Preview"
          className={cn(
            "rounded-lg object-cover",
            compact ? "h-24 w-24" : "h-40 w-40"
          )}
        />
      ) : (
        <>
          <div
            className={cn(
              "flex items-center justify-center rounded-xl bg-primary/10",
              compact ? "h-10 w-10" : "h-14 w-14"
            )}
          >
            {compact ? (
              <ImageIcon className="h-5 w-5 text-primary" />
            ) : (
              <Upload className="h-6 w-6 text-primary" />
            )}
          </div>
          <div className="text-center">
            <p
              className={cn(
                "font-medium text-foreground",
                compact ? "text-xs" : "text-sm"
              )}
            >
              {label}
            </p>
            <p
              className={cn(
                "text-muted-foreground",
                compact ? "text-[10px]" : "text-xs"
              )}
            >
              {sublabel}
            </p>
          </div>
        </>
      )}
      <input
        type="file"
        accept={accept}
        onChange={handleChange}
        className="hidden"
      />
    </label>
  );
}
