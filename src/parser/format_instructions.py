from typing import List, Optional, Literal
from datetime import date
from pydantic import BaseModel, Field

class Party(BaseModel):
    """
    Represents an entity involved in the transaction, such as supplier or customer.
    """
    name: Optional[str] = Field(None, description="Full name of the party")
    address: Optional[str] = Field(None, description="Postal address of the party")
    email: Optional[str] = Field(None, description="Contact email address")
    phone: Optional[str] = Field(
        None,
        description="Contact phone number; include country code if needed"
    )
    tax_id: Optional[str] = Field(None, description="Tax identification number, if available")

class Item(BaseModel):
    """
    Represents a single line item in the invoice or receipt.
    """
    description: Optional[str] = Field(None, description="Description of the product or service")
    quantity: Optional[float] = Field(None, gt=0, description="Quantity of the item; must be greater than 0")
    unit_price: Optional[float] = Field(None, ge=0, description="Price per unit; must be non-negative")
    total_price: Optional[float] = Field(None, ge=0, description="Total for this line; typically quantity * unit_price")
    tax_rate: Optional[float] = Field(0.0, ge=0, le=1, description="Tax rate as a decimal (e.g., 0.10 for 10%)")
    tax_amount: Optional[float] = Field(0.0, ge=0, description="Calculated tax amount for this line")

class Totals(BaseModel):
    """
    Aggregated financial totals for the document.
    """
    subtotal: Optional[float] = Field(None, ge=0, description="Sum of all line item totals before tax and discounts")
    tax_total: Optional[float] = Field(None, ge=0, description="Total tax amount for all items")
    discount: Optional[float] = Field(0, ge=0, description="Total discount applied, if any")
    shipping: Optional[float] = Field(0, ge=0, description="Shipping or handling charges, if any")
    grand_total: Optional[float] = Field(None, ge=0, description="Total due including taxes, shipping, and discounts")
    amount_paid: Optional[float] = Field(0, ge=0, description="Amount already paid toward this document")
    balance_due: Optional[float] = Field(None, ge=0, description="Remaining balance after payments")

class Payment(BaseModel):
    """
    Details about the payment for the invoice or receipt.
    """
    method: Optional[str] = Field(None, description="Payment method (e.g., Credit Card, Bank Transfer)")
    transaction_id: Optional[str] = Field(None, description="Identifier for the payment transaction")
    payment_date: Optional[str] = Field(None, description="Date when payment was made")

class InvoiceReceipt(BaseModel):
    """
    Master schema for any invoice or receipt document.
    """
    document_type: Literal['invoice', 'receipt'] = Field(
        description="Type of document: 'invoice' or 'receipt'"
    )
    document_number: Optional[str] = Field(None, description="Unique identifier of the document")
    issue_date: Optional[str] = Field(None, description="Date when the document was issued")
    due_date: Optional[str] = Field(None, description="Payment due date; applicable for invoices")
    currency: Optional[str] = Field(
        None, description="Three-letter currency code (e.g., USD, EUR)"
    )
    supplier: Optional[Party] = Field(None, description="Entity issuing the document")
    customer: Optional[Party] = Field(None, description="Entity receiving the goods or services")
    items: Optional[List[Item]] = Field(None, description="List of items or services provided")
    totals: Optional[Totals] = Field(None, description="Aggregated financial totals for the document")
    payment: Optional[Payment] = Field(None, description="Payment details, if payment has been recorded")
    notes: Optional[str] = Field(None, description="Additional remarks or notes about the transaction")
