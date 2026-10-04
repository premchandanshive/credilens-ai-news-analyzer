import { useRef, useState } from 'react';
import { ArrowRight, Link2, Upload } from 'lucide-react';
import { looksLikeUrl, validateFile, validateText, validateUrl } from '../utils/validation.js';

export default function AnalysisInput({ onSubmit, disabled, compact }) {
  const [mode, setMode] = useState('text');
  const [text, setText] = useState('');
  const [url, setUrl] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const fileRef = useRef(null);

  function handlePasteUrl() {
    setMode('url');
    setError(null);
  }

  function handleUploadClick() {
    setMode('file');
    fileRef.current?.click();
  }

  function onFileChange(event) {
    const next = event.target.files?.[0] || null;
    setFile(next);
    setError(next ? validateFile(next) : null);
  }

  function submit(event) {
    event.preventDefault();
    if (mode === 'url' || looksLikeUrl(text)) {
      const value = mode === 'url' ? url : text;
      const message = validateUrl(value);
      setError(message);
      if (message) return;
      onSubmit({ kind: 'url', url: value.trim() });
      return;
    }
    if (mode === 'file') {
      const message = validateFile(file);
      setError(message);
      if (message) return;
      onSubmit({ kind: 'file', file });
      return;
    }
    const message = validateText(text);
    setError(message);
    if (message) return;
    onSubmit({ kind: 'text', text: text.trim() });
  }

  return (
    <form onSubmit={submit} className="card-surface p-4 lg:p-5">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <h2 className="text-sm font-semibold lg:text-base">Analyze News or Claim</h2>
          <p className="text-xs text-muted mt-1">Paste article link, claim or text to check credibility</p>
        </div>
      </div>

      <label className="sr-only" htmlFor="analysis-input">
        Article text or URL
      </label>
      {mode !== 'file' ? (
        <textarea
          id="analysis-input"
          rows={compact ? 4 : 5}
          value={mode === 'url' ? url : text}
          onChange={(e) => {
            if (mode === 'url') setUrl(e.target.value);
            else setText(e.target.value);
            setError(null);
          }}
          placeholder={mode === 'url' ? 'https://example.com/news-article' : 'Paste news article link or text here…'}
          className="w-full resize-y rounded-xl border border-cred-border bg-cred-bg px-3 py-3 text-sm placeholder:text-cred-muted focus:border-cred-accent"
          disabled={disabled}
        />
      ) : (
        <button
          type="button"
          onClick={() => fileRef.current?.click()}
          className="w-full rounded-xl border border-dashed border-cred-border-strong bg-cred-bg px-3 py-8 text-sm text-muted hover:border-cred-accent"
        >
          {file ? file.name : 'Choose a .txt, .md, or .pdf file (max 5 MB)'}
        </button>
      )}

      <input
        ref={fileRef}
        type="file"
        accept=".txt,.md,.pdf,text/plain,application/pdf"
        className="hidden"
        onChange={onFileChange}
      />

      {error ? <p className="mt-2 text-sm text-cred-danger">{error}</p> : null}

      <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex gap-2">
          <button
            type="button"
            onClick={handlePasteUrl}
            className={`inline-flex items-center gap-2 rounded-xl border px-3 py-2 text-xs ${
              mode === 'url' ? 'border-cred-accent text-cred-text bg-cred-accent-soft' : 'border-cred-border text-muted'
            }`}
          >
            <Link2 size={14} />
            Paste URL
          </button>
          <button
            type="button"
            onClick={handleUploadClick}
            className={`inline-flex items-center gap-2 rounded-xl border px-3 py-2 text-xs ${
              mode === 'file' ? 'border-cred-accent text-cred-text bg-cred-accent-soft' : 'border-cred-border text-muted'
            }`}
          >
            <Upload size={14} />
            Upload File
          </button>
          {mode !== 'text' ? (
            <button
              type="button"
              onClick={() => {
                setMode('text');
                setError(null);
              }}
              className="rounded-xl border border-cred-border px-3 py-2 text-xs text-muted"
            >
              Use text
            </button>
          ) : null}
        </div>
        <button
          type="submit"
          disabled={disabled}
          className="inline-flex items-center justify-center gap-2 rounded-xl bg-cred-accent px-5 py-2.5 text-sm font-medium text-white hover:bg-cred-accent-hover disabled:opacity-50"
        >
          Analyze
          <ArrowRight size={16} />
        </button>
      </div>
    </form>
  );
}
