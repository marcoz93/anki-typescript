// 1–6: valores, tipos e representação dos dados.
type Refund = {
  id: string;
  amount: number;
};
type ReviewStatus = "required" | "not_required";
const reviewLimit: number = 10000;
const refunds: Refund[] = [
  { id: "reembolso-01", amount: 15000 },
  { id: "reembolso-02", amount: 5000 },
  { id: "reembolso-03", amount: 10000 },
];

// 7–9: funções, invocação e composição.
function getRefundAmount(item: Refund): number {
  return item.amount;
}
function isAboveLimit(amount: number, limit: number): boolean {
  return amount > limit;
}
function isReviewRequired(item: Refund, limit: number): boolean {
  return isAboveLimit(getRefundAmount(item), limit);
}

// 10: função como valor, com limite fixado para a coleção.
const needsReview = (item: Refund): boolean =>
  isReviewRequired(item, reviewLimit);

// 11–12: união literal e seleção condicional.
function classifyRefund(item: Refund, limit: number): ReviewStatus {
  if (isReviewRequired(item, limit)) {
    return "required";
  } else {
    return "not_required";
  }
}

// 13: ausência e estreitamento de tipos.
function getReviewStatus(item: Refund | undefined, limit: number): ReviewStatus | undefined {
  if (item === undefined) {
    return undefined;
  }
  return classifyRefund(item, limit);
}

// 14: transformação e consulta de coleções.
const statuses = refunds.map((item) => classifyRefund(item, reviewLimit));
const requiredRefunds = refunds.filter(needsReview);
const foundRefund = refunds.find((item) => item.id === "reembolso-02");
const foundStatus = getReviewStatus(foundRefund, reviewLimit);
const missingRefund = refunds.find((item) => item.id === "reembolso-99");

console.log(statuses);
console.log(requiredRefunds);
console.log(foundStatus);
console.log(getReviewStatus(missingRefund, reviewLimit));

// 15: iteração explícita para apresentar os resultados.
for (const item of requiredRefunds) {
  console.log(item.id);
}
