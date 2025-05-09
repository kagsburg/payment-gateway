<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class PaymentRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
           'payer' => 'required|numeric|digits:10',
            'payee' => 'required|numeric|digits:10',
            'amount' => 'required|numeric|min:0.01',
            'currency' => 'required|string|size:3',
            'payer_reference' => 'nullable|string|max:255'
        ];
    }
}
