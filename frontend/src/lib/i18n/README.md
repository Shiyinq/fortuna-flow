# Sistem Multi-Language (i18n)

Sistem multi-language ini memungkinkan aplikasi untuk mendukung berbagai bahasa dengan mudah.

## Fitur

- ✅ Dukungan multi-language untuk seluruh aplikasi
- ✅ Perubahan bahasa secara real-time
- ✅ Penyimpanan preferensi bahasa di localStorage
- ✅ Komponen language selector yang mudah digunakan
- ✅ Hook Svelte untuk menggunakan terjemahan
- ✅ Template untuk menambahkan bahasa baru

## Bahasa yang Tersedia

- 🇮🇩 Bahasa Indonesia (id)
- 🇺🇸 English (en)

## Cara Menggunakan

### 1. Menggunakan Terjemahan dalam Komponen

```svelte
<script>
  import { useTranslation } from '$lib/i18n/useTranslation';
  
  const { t } = useTranslation();
</script>

<h1>{$t('navigation.home')}</h1>
<p>{$t('common.loading')}</p>
```

### 2. Menggunakan Fungsi Terjemahan Langsung

```typescript
import { t } from '$lib/i18n';

const message = t('auth.signinSuccess');
```

### 3. Mengubah Bahasa

```typescript
import { changeLanguage } from '$lib/i18n';

// Mengubah ke bahasa Inggris
changeLanguage('en');

// Mengubah ke bahasa Indonesia
changeLanguage('id');
```

## Menambahkan Bahasa Baru

### Langkah 1: Buat File Terjemahan

1. Salin file `template.json` dan beri nama sesuai kode bahasa (misal: `ja.json` untuk bahasa Jepang)
2. Edit file tersebut dengan terjemahan yang sesuai

### Langkah 2: Update Konfigurasi

1. Buka file `frontend/src/lib/i18n/index.ts`
2. Import file terjemahan baru:

```typescript
import ja from './locales/ja.json';
```

3. Tambahkan ke daftar bahasa yang tersedia:

```typescript
export const availableLanguages = [
  { code: 'id', name: 'Bahasa Indonesia', flag: '🇮🇩' },
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'ja', name: '日本語', flag: '🇯🇵' } // Tambahkan ini
];
```

4. Tambahkan ke fungsi `loadTranslations`:

```typescript
const loadTranslations = (lang: string) => {
  switch (lang) {
    case 'id':
      return id;
    case 'en':
      return en;
    case 'ja':
      return ja; // Tambahkan ini
    default:
      return id;
  }
};
```

### Langkah 3: Test

1. Restart development server
2. Buka aplikasi dan cek apakah bahasa baru muncul di language selector
3. Test perubahan bahasa

## Struktur File Terjemahan

File terjemahan menggunakan struktur nested untuk organisasi yang lebih baik:

```json
{
  "common": {
    "loading": "Loading...",
    "save": "Save"
  },
  "auth": {
    "signin": "Sign In",
    "signup": "Sign Up"
  },
  "navigation": {
    "home": "Home",
    "transactions": "Transactions"
  }
}
```

## Kunci Terjemahan

### Common
- `loading` - Teks loading
- `save` - Tombol simpan
- `cancel` - Tombol batal
- `delete` - Tombol hapus
- `edit` - Tombol edit
- `add` - Tombol tambah
- `close` - Tombol tutup
- `back` - Tombol kembali
- `next` - Tombol selanjutnya
- `previous` - Tombol sebelumnya
- `search` - Placeholder pencarian
- `filter` - Tombol filter
- `sort` - Tombol urutkan
- `all` - Teks "semua"
- `none` - Teks "tidak ada"
- `yes` - Teks "ya"
- `no` - Teks "tidak"
- `ok` - Tombol OK
- `error` - Label error
- `success` - Label sukses
- `warning` - Label peringatan
- `info` - Label informasi

### Auth
- `signin` - Tombol masuk
- `signup` - Tombol daftar
- `signout` - Tombol keluar
- `email` - Label email
- `password` - Label kata sandi
- `confirmPassword` - Label konfirmasi kata sandi
- `forgotPassword` - Link lupa kata sandi
- `resetPassword` - Judul reset kata sandi
- `sendVerification` - Tombol kirim verifikasi
- `verifyEmail` - Judul verifikasi email
- `dontHaveAccount` - Teks belum punya akun
- `alreadyHaveAccount` - Teks sudah punya akun
- `signinHere` - Link masuk di sini
- `signupHere` - Link daftar di sini
- `emailRequired` - Pesan error email wajib
- `passwordRequired` - Pesan error kata sandi wajib
- `passwordMinLength` - Pesan error minimal karakter
- `passwordMismatch` - Pesan error kata sandi tidak cocok
- `invalidEmail` - Pesan error email tidak valid
- `signinSuccess` - Pesan sukses masuk
- `signupSuccess` - Pesan sukses daftar
- `signoutSuccess` - Pesan sukses keluar
- `verificationSent` - Pesan email verifikasi terkirim
- `passwordResetSent` - Pesan email reset terkirim
- `emailVerified` - Pesan email terverifikasi

### Navigation
- `home` - Menu beranda
- `transactions` - Menu transaksi
- `budgets` - Menu anggaran
- `categories` - Menu kategori
- `wallets` - Menu dompet
- `profile` - Menu profil
- `reports` - Menu laporan
- `settings` - Menu pengaturan

### Transactions
- `title` - Judul halaman transaksi
- `addTransaction` - Tombol tambah transaksi
- `editTransaction` - Tombol edit transaksi
- `deleteTransaction` - Tombol hapus transaksi
- `amount` - Label jumlah
- `type` - Label tipe
- `category` - Label kategori
- `wallet` - Label dompet
- `date` - Label tanggal
- `note` - Label catatan
- `income` - Tipe pemasukan
- `expense` - Tipe pengeluaran
- `transfer` - Tipe transfer
- `recentTransactions` - Judul transaksi terbaru
- `noTransactions` - Pesan tidak ada transaksi
- `transactionAdded` - Pesan sukses tambah transaksi
- `transactionUpdated` - Pesan sukses update transaksi
- `transactionDeleted` - Pesan sukses hapus transaksi
- `selectCategory` - Placeholder pilih kategori
- `selectWallet` - Placeholder pilih dompet
- `enterAmount` - Placeholder masukkan jumlah
- `enterNote` - Placeholder masukkan catatan

### Budgets
- `title` - Judul halaman anggaran
- `addBudget` - Tombol tambah anggaran
- `editBudget` - Tombol edit anggaran
- `deleteBudget` - Tombol hapus anggaran
- `budgetName` - Label nama anggaran
- `budgetAmount` - Label jumlah anggaran
- `budgetPeriod` - Label periode anggaran
- `budgetCategory` - Label kategori anggaran
- `budgetUsed` - Label terpakai
- `budgetRemaining` - Label sisa
- `budgetProgress` - Label progress
- `noBudgets` - Pesan tidak ada anggaran
- `budgetAdded` - Pesan sukses tambah anggaran
- `budgetUpdated` - Pesan sukses update anggaran
- `budgetDeleted` - Pesan sukses hapus anggaran
- `monthly` - Periode bulanan
- `yearly` - Periode tahunan
- `weekly` - Periode mingguan
- `daily` - Periode harian

### Categories
- `title` - Judul halaman kategori
- `addCategory` - Tombol tambah kategori
- `editCategory` - Tombol edit kategori
- `deleteCategory` - Tombol hapus kategori
- `categoryName` - Label nama kategori
- `categoryIcon` - Label ikon kategori
- `categoryColor` - Label warna kategori
- `noCategories` - Pesan tidak ada kategori
- `categoryAdded` - Pesan sukses tambah kategori
- `categoryUpdated` - Pesan sukses update kategori
- `categoryDeleted` - Pesan sukses hapus kategori
- `selectIcon` - Placeholder pilih ikon
- `selectColor` - Placeholder pilih warna

### Wallets
- `title` - Judul halaman dompet
- `addWallet` - Tombol tambah dompet
- `editWallet` - Tombol edit dompet
- `deleteWallet` - Tombol hapus dompet
- `walletName` - Label nama dompet
- `walletIcon` - Label ikon dompet
- `walletBalance` - Label saldo dompet
- `walletCurrency` - Label mata uang
- `noWallets` - Pesan tidak ada dompet
- `walletAdded` - Pesan sukses tambah dompet
- `walletUpdated` - Pesan sukses update dompet
- `walletDeleted` - Pesan sukses hapus dompet
- `selectCurrency` - Placeholder pilih mata uang
- `allWallets` - Label semua dompet

### Profile
- `title` - Judul halaman profil
- `personalInfo` - Judul informasi pribadi
- `accountSettings` - Judul pengaturan akun
- `preferences` - Judul preferensi
- `firstName` - Label nama depan
- `lastName` - Label nama belakang
- `fullName` - Label nama lengkap
- `phone` - Label telepon
- `address` - Label alamat
- `language` - Label bahasa
- `timezone` - Label zona waktu
- `currency` - Label mata uang
- `darkMode` - Label mode gelap
- `notifications` - Label notifikasi
- `saveChanges` - Tombol simpan perubahan
- `profileUpdated` - Pesan sukses update profil

### Reports
- `title` - Judul halaman laporan
- `incomeVsExpense` - Judul pemasukan vs pengeluaran
- `categoryBreakdown` - Judul rincian kategori
- `monthlyTrend` - Judul tren bulanan
- `yearlySummary` - Judul ringkasan tahunan
- `topCategories` - Judul kategori teratas
- `totalIncome` - Label total pemasukan
- `totalExpense` - Label total pengeluaran
- `netIncome` - Label pendapatan bersih
- `averagePerDay` - Label rata-rata per hari
- `averagePerMonth` - Label rata-rata per bulan
- `noData` - Pesan tidak ada data
- `selectPeriod` - Placeholder pilih periode
- `thisMonth` - Periode bulan ini
- `lastMonth` - Periode bulan lalu
- `thisYear` - Periode tahun ini
- `lastYear` - Periode tahun lalu
- `custom` - Periode kustom

### Language
- `title` - Judul bahasa
- `selectLanguage` - Placeholder pilih bahasa
- `languageChanged` - Pesan sukses ubah bahasa

## Best Practices

1. **Gunakan kunci yang deskriptif**: `auth.signin` lebih baik daripada `signin`
2. **Kelompokkan terjemahan**: Gunakan struktur nested untuk organisasi yang lebih baik
3. **Gunakan placeholder untuk variabel**: `Hello {name}` bukan `Hello John`
4. **Test semua bahasa**: Pastikan semua bahasa terlihat baik di UI
5. **Gunakan emoji bendera**: Untuk identifikasi bahasa yang lebih mudah

## Troubleshooting

### Bahasa tidak berubah
- Pastikan file terjemahan sudah diimport dengan benar
- Cek apakah kode bahasa sudah ditambahkan ke `availableLanguages`
- Restart development server

### Terjemahan tidak muncul
- Pastikan kunci terjemahan sudah benar
- Cek apakah struktur JSON sudah valid
- Gunakan `console.log` untuk debug

### Error TypeScript
- Pastikan tipe data sudah benar di `useTranslation`
- Cek apakah semua import sudah benar 