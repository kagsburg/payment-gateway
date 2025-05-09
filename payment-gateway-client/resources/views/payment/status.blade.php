@extends('layout.app')

@section('title', 'Payment Status')

@section('content')
    <div class="max-w-md mx-auto">
        @if ($transaction['status_code'] == 100)
            <div class="p-4 mb-6 bg-blue-100 border border-blue-400 text-blue-700 rounded-lg">
                {{ $transaction['message'] }}
            </div>
        @elseif ($transaction['status_code'] == 200)
            <div class="p-4 mb-6 bg-green-100 border border-green-400 text-green-700 rounded-lg">
                {{ $transaction['message'] }}
            </div>
        @else
            <div class="p-4 mb-6 bg-red-100 border border-red-400 text-red-700 rounded-lg">
                {{ $transaction['message'] }}
            </div>
        @endif

        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                    Transaction Details
                </h3>
            </div>
            <div class="px-4 py-5 sm:p-6">
                <dl class="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
                    <div class="sm:col-span-1">
                        <dt class="text-sm font-medium text-gray-500">Reference</dt>
                        <dd class="mt-1 text-sm text-gray-900 break-words">{{ $transaction['transaction_reference'] }}</dd>
                    </div>
                    <div class="sm:col-span-1">
                        <dt class="text-sm font-medium text-gray-500">Status Code</dt>
                        <dd class="mt-1 text-sm text-gray-900">{{ $transaction['status_code'] }}</dd>
                    </div>
                </dl>
            </div>
        </div>

        <div class="mt-6">
            <a href="{{ route('payment.form') }}"
               class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                Make Another Payment
            </a>
        </div>
    </div>
@endsection