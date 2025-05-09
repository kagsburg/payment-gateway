@extends('layout.app')

@section('title', 'Initiate Payment')

@section('content')
   <div class="w-full max-w-sm mx-auto p-6 bg-white rounded-lg shadow">
    @if (session('error'))
        <div class="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            {{ session('error') }}
        </div>
    @endif
<div x-data="{ loading: false }">
    <form method="POST" action="{{ route('payment.process') }}" @submit="loading = true" class="space-y-6">
        @csrf
           
            <div>
                <label for="payer" class="block text-sm font-medium text-gray-700">Payer Account</label>
                <input id="payer" type="text" name="payer" value="{{ old('payer') }}" 
                       class="h-12 text-base mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500" 
                       required autocomplete="off" maxlength="10">
                @error('payer')
                    <p class="mt-2 text-sm text-red-600">{{ $message }}</p>
                @enderror
            </div>

       <!-- Similar fields for payee, amount, currency -->
            <div>
                <label for="payee" class="block text-sm font-medium text-gray-700">Payee Account</label>
                <input id="payee" type="text" name="payee" value="{{ old('payee') }}"
                       class="h-12 text-base mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                       required autocomplete="off" maxlength="10">
                @error('payee')
                    <p class="mt-2 text-sm text-red-600">{{ $message }}</p>
                @enderror
            </div>
            <div>
                <label for="amount" class="block text-sm font-medium text-gray-700">Amount</label>
                <input id="amount" type="number" step="0.01" name="amount" value="{{ old('amount') }}"
                       class="h-12 text-base mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                       required min="0.01">
                @error('amount')
                    <p class="mt-2 text-sm text-red-600">{{ $message }}</p>
                @enderror
            </div>
             <div>
                <label for="currency" class="block text-sm font-medium text-gray-700">Currency</label>
                <select id="currency" name="currency"
                        class="h-12 text-base mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                        required>
                    <option value="">Select Currency</option>
                    <option value="UGX" {{ old('currency') == 'UGX' ? 'selected' : '' }}>UGX</option>
                    <option value="USD" {{ old('currency') == 'USD' ? 'selected' : '' }}>USD</option>
                    <option value="EUR" {{ old('currency') == 'EUR' ? 'selected' : '' }}>EUR</option>
                    <option value="GBP" {{ old('currency') == 'GBP' ? 'selected' : '' }}>GBP</option>                    
                </select>
                @error('currency')
                    <p class="mt-2 text-sm text-red-600">{{ $message }}</p>
                @enderror
            </div>
            <div>
                <label for="payer_reference" class="block text-sm font-medium text-gray-700">Reason</label>
                <input id="payer_reference" type="text" name="payer_reference" value="{{ old('payer_reference') }}"
                       class="h-12 text-base mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                       maxlength="255">
            </div>

        <div>
            <button type="submit"
                    x-bind:disabled="loading"
                    class="w-full flex justify-center items-center gap-2 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50">
                <svg x-show="loading" class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10"
                            stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                          d="M4 12a8 8 0 018-8v8z"></path>
                </svg>
                <span x-text="loading ? 'Processing...' : 'Submit Payment'"></span>
            </button>
        </div>
    </form>
    </div>
</div>

@endsection