/** @typedef {'text' | 'url' | 'file'} InputType */

/** @typedef {'likely_reliable' | 'likely_unreliable' | 'uncertain'} PredictionLabel */

/** @typedef {'SUPPORTED' | 'CONTRADICTED' | 'INSUFFICIENT_EVIDENCE'} ClaimStatus */

/** @typedef {'positive' | 'warning' | 'negative' | 'info'} FindingTone */

/** @typedef {'supports' | 'contradicts' | 'related' | 'insufficient'} SourceRelationship */

/**
 * @typedef {Object} ApiError
 * @property {string} code
 * @property {string} message
 */

/**
 * @typedef {Object} ApiEnvelope
 * @property {boolean} success
 * @property {any} data
 * @property {ApiError | null} error
 */

/**
 * @typedef {Object} AnalysisProgressEvent
 * @property {string} stage
 * @property {string} label
 * @property {boolean} done
 */

/**
 * @typedef {Object} Claim
 * @property {string} id
 * @property {string} text
 * @property {ClaimStatus} status
 * @property {number} [confidence]
 * @property {string[]} [evidenceIds]
 */

/**
 * @typedef {Object} SourceItem
 * @property {string} [id]
 * @property {string} title
 * @property {string} url
 * @property {string} domain
 * @property {string | null} [publisher]
 * @property {string | null} [author]
 * @property {string | null} [publishedAt]
 * @property {string} excerpt
 * @property {number} relevanceScore
 * @property {number} transparencyScore
 * @property {SourceRelationship} relationship
 */

/**
 * @typedef {Object} Finding
 * @property {FindingTone} tone
 * @property {string} text
 * @property {'evidence' | 'language' | 'model' | 'source'} basis
 */

/**
 * @typedef {Object} AnalysisResult
 * @property {string} id
 * @property {string | null} [userId]
 * @property {InputType} inputType
 * @property {string | null} [inputText]
 * @property {string | null} [inputUrl]
 * @property {string | null} [fileName]
 * @property {string} title
 * @property {string} [articleExcerpt]
 * @property {{ label: PredictionLabel, modelName: string, probabilities: Record<string, number>, aiClassificationScore: number }} prediction
 * @property {number} credibilityScore
 * @property {string} credibilityBand
 * @property {string} disclaimer
 * @property {{ aiClassification: number, evidenceVerification: number, sourceAnalysis: number, languageAnalysis: number, claimConsistency: number }} componentScores
 * @property {Record<string, number>} [weightsUsed]
 * @property {Claim[]} claims
 * @property {SourceItem[]} sources
 * @property {{ sensationalismScore: number, emotionalLanguage: string, clickbaitIndicators: string, absoluteClaimCount: number, signals: string[] }} languageAnalysis
 * @property {{ findings: Finding[], modelExplanation: { method: string, topFeatures: { feature: string, weight: number }[] } }} explanation
 * @property {{ entities: { text: string, label: string }[], claimCount: number }} [nlp]
 * @property {'completed' | 'failed' | 'partial'} status
 * @property {ApiError | null} [error]
 * @property {string} createdAt
 */

/**
 * @typedef {Object} HistoryPage
 * @property {AnalysisResult[]} items
 * @property {number} total
 * @property {number} page
 * @property {number} limit
 */

/**
 * @typedef {Object} SystemStatus
 * @property {boolean} api
 * @property {boolean} database
 * @property {boolean} models
 * @property {boolean} nlp
 * @property {boolean} evidence
 * @property {boolean} searchKeyConfigured
 */

/**
 * @typedef {Object} UserProfile
 * @property {string} id
 * @property {string} email
 * @property {string} displayName
 * @property {string} [role]
 * @property {{ theme: 'dark' | 'light', maxClaims: number, includeTransformer: boolean }} preferences
 */

export {};
