import os

from cffi import FFI

BASE_DEFINITIONS = """
typedef struct secp256k1_context_struct secp256k1_context;

typedef struct {
    unsigned char data[64];
} secp256k1_pubkey;

typedef struct {
    unsigned char data[64];
} secp256k1_ecdsa_signature;

typedef int (*secp256k1_nonce_function)(
    unsigned char *nonce32,
    const unsigned char *msg32,
    const unsigned char *key32,
    const unsigned char *algo16,
    void *data,
    unsigned int attempt
);

#define SECP256K1_FLAGS_TYPE_MASK 255
#define SECP256K1_FLAGS_TYPE_CONTEXT 1
#define SECP256K1_FLAGS_TYPE_COMPRESSION 2

#define SECP256K1_FLAGS_BIT_CONTEXT_VERIFY 256
#define SECP256K1_FLAGS_BIT_CONTEXT_SIGN 512
#define SECP256K1_FLAGS_BIT_COMPRESSION 256

#define SECP256K1_CONTEXT_VERIFY 257
#define SECP256K1_CONTEXT_SIGN 513
#define SECP256K1_CONTEXT_NONE 1

#define SECP256K1_EC_COMPRESSED 258
#define SECP256K1_EC_UNCOMPRESSED 2

secp256k1_context* secp256k1_context_create(
    unsigned int flags
);

secp256k1_context* secp256k1_context_clone(
    const secp256k1_context* ctx
);

void secp256k1_context_destroy(
    secp256k1_context* ctx
);

void secp256k1_context_set_illegal_callback(
    secp256k1_context* ctx,
    void (*fun)(const char* message, void* data),
    const void* data
);

void secp256k1_context_set_error_callback(
    secp256k1_context* ctx,
    void (*fun)(const char* message, void* data),
    const void* data
);

int secp256k1_ec_pubkey_parse(
    const secp256k1_context* ctx,
    secp256k1_pubkey* pubkey,
    const unsigned char *input,
    size_t inputlen
);

int secp256k1_ec_pubkey_serialize(
    const secp256k1_context* ctx,
    unsigned char *output,
    size_t *outputlen,
    const secp256k1_pubkey* pubkey,
    unsigned int flags
);

int secp256k1_ecdsa_signature_parse_compact(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_signature* sig,
    const unsigned char *input64
);

int secp256k1_ecdsa_signature_parse_der(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_signature* sig,
    const unsigned char *input,
    size_t inputlen
);

int secp256k1_ecdsa_signature_serialize_der(
    const secp256k1_context* ctx,
    unsigned char *output,
    size_t *outputlen,
    const secp256k1_ecdsa_signature* sig
);

int secp256k1_ecdsa_signature_serialize_compact(
    const secp256k1_context* ctx,
    unsigned char *output64,
    const secp256k1_ecdsa_signature* sig
);

int secp256k1_ecdsa_verify(
    const secp256k1_context* ctx,
    const secp256k1_ecdsa_signature *sig,
    const unsigned char *msg32,
    const secp256k1_pubkey *pubkey
);

int secp256k1_ecdsa_signature_normalize(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_signature *sigout,
    const secp256k1_ecdsa_signature *sigin
);

extern const secp256k1_nonce_function secp256k1_nonce_function_rfc6979;

extern const secp256k1_nonce_function secp256k1_nonce_function_default;

int secp256k1_ecdsa_sign(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_signature *sig,
    const unsigned char *msg32,
    const unsigned char *seckey,
    secp256k1_nonce_function noncefp,
    const void *ndata
);

int secp256k1_ec_seckey_verify(
    const secp256k1_context* ctx,
    const unsigned char *seckey
);

int secp256k1_ec_pubkey_create(
    const secp256k1_context* ctx,
    secp256k1_pubkey *pubkey,
    const unsigned char *seckey
);

int secp256k1_ec_privkey_tweak_add(
    const secp256k1_context* ctx,
    unsigned char *seckey,
    const unsigned char *tweak
);

int secp256k1_ec_pubkey_tweak_add(
    const secp256k1_context* ctx,
    secp256k1_pubkey *pubkey,
    const unsigned char *tweak
);

int secp256k1_ec_privkey_tweak_mul(
    const secp256k1_context* ctx,
    unsigned char *seckey,
    const unsigned char *tweak
);

int secp256k1_ec_pubkey_tweak_mul(
    const secp256k1_context* ctx,
    secp256k1_pubkey *pubkey,
    const unsigned char *tweak
);

int secp256k1_context_randomize(
    secp256k1_context* ctx,
    const unsigned char *seed32
);

int secp256k1_ec_pubkey_combine(
    const secp256k1_context* ctx,
    secp256k1_pubkey *out,
    const secp256k1_pubkey * const * ins,
    size_t n
);
"""

EXTRAKEYS_DEFINITIONS = """
typedef struct {
    unsigned char data[64];
} secp256k1_xonly_pubkey;

typedef struct {
    unsigned char data[96];
} secp256k1_keypair;

int secp256k1_xonly_pubkey_parse(
    const secp256k1_context* ctx,
    secp256k1_xonly_pubkey* pubkey,
    const unsigned char *input32
);

int secp256k1_xonly_pubkey_serialize(
    const secp256k1_context* ctx,
    unsigned char *output32,
    const secp256k1_xonly_pubkey* pubkey
);

int secp256k1_xonly_pubkey_cmp(
    const secp256k1_context* ctx,
    const secp256k1_xonly_pubkey* pk1,
    const secp256k1_xonly_pubkey* pk2
);

int secp256k1_xonly_pubkey_from_pubkey(
    const secp256k1_context* ctx,
    secp256k1_xonly_pubkey *xonly_pubkey,
    int *pk_parity,
    const secp256k1_pubkey *pubkey
);

int secp256k1_xonly_pubkey_tweak_add(
    const secp256k1_context* ctx,
    secp256k1_pubkey *output_pubkey,
    const secp256k1_xonly_pubkey *internal_pubkey,
    const unsigned char *tweak32
);

int secp256k1_xonly_pubkey_tweak_add_check(
    const secp256k1_context* ctx,
    const unsigned char *tweaked_pubkey32,
    int tweaked_pk_parity,
    const secp256k1_xonly_pubkey *internal_pubkey,
    const unsigned char *tweak32
);

int secp256k1_keypair_create(
    const secp256k1_context* ctx,
    secp256k1_keypair *keypair,
    const unsigned char *seckey
);

int secp256k1_keypair_sec(
    const secp256k1_context* ctx,
    unsigned char *seckey,
    const secp256k1_keypair *keypair
);

int secp256k1_keypair_pub(
    const secp256k1_context* ctx,
    secp256k1_pubkey *pubkey,
    const secp256k1_keypair *keypair
);

int secp256k1_keypair_xonly_pub(
    const secp256k1_context* ctx,
    secp256k1_xonly_pubkey *pubkey,
    int *pk_parity,
    const secp256k1_keypair *keypair
);

int secp256k1_keypair_xonly_tweak_add(
    const secp256k1_context* ctx,
    secp256k1_keypair *keypair,
    const unsigned char *tweak32
);
"""

RECOVERY_DEFINITIONS = """
typedef struct {
    unsigned char data[65];
} secp256k1_ecdsa_recoverable_signature;

int secp256k1_ecdsa_recoverable_signature_parse_compact(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_recoverable_signature* sig,
    const unsigned char *input64,
    int recid
);

int secp256k1_ecdsa_recoverable_signature_convert(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_signature* sig,
    const secp256k1_ecdsa_recoverable_signature* sigin
);

int secp256k1_ecdsa_recoverable_signature_serialize_compact(
    const secp256k1_context* ctx,
    unsigned char *output64,
    int *recid,
    const secp256k1_ecdsa_recoverable_signature* sig
);

int secp256k1_ecdsa_sign_recoverable(
    const secp256k1_context* ctx,
    secp256k1_ecdsa_recoverable_signature *sig,
    const unsigned char *msg32,
    const unsigned char *seckey,
    secp256k1_nonce_function noncefp,
    const void *ndata
);

int secp256k1_ecdsa_recover(
    const secp256k1_context* ctx,
    secp256k1_pubkey *pubkey,
    const secp256k1_ecdsa_recoverable_signature *sig,
    const unsigned char *msg32
);
"""

SCHNORRSIG_DEFINITIONS = """
typedef int (*secp256k1_nonce_function_hardened)(
    unsigned char *nonce32,
    const unsigned char *msg,
    size_t msglen,
    const unsigned char *key32,
    const unsigned char *xonly_pk32,
    const unsigned char *algo,
    size_t algolen,
    void *data
);

extern const secp256k1_nonce_function_hardened secp256k1_nonce_function_bip340;

typedef struct {
    unsigned char magic[4];
    secp256k1_nonce_function_hardened noncefp;
    void* ndata;
} secp256k1_schnorrsig_extraparams;

int secp256k1_schnorrsig_sign(
    const secp256k1_context* ctx,
    unsigned char *sig64,
    const unsigned char *msg32,
    const secp256k1_keypair *keypair,
    const unsigned char *aux_rand32
);

int secp256k1_schnorrsig_sign32(
    const secp256k1_context* ctx,
    unsigned char *sig64,
    const unsigned char *msg32,
    const secp256k1_keypair *keypair,
    const unsigned char *aux_rand32
);

int secp256k1_schnorrsig_sign_custom(
    const secp256k1_context* ctx,
    unsigned char *sig64,
    const unsigned char *msg,
    size_t msglen,
    const secp256k1_keypair *keypair,
    secp256k1_schnorrsig_extraparams *extraparams
);

int secp256k1_schnorrsig_verify(
    const secp256k1_context* ctx,
    const unsigned char *sig64,
    const unsigned char *msg,
    size_t msglen,
    const secp256k1_xonly_pubkey *pubkey
);
"""

ECDH_DEFINITIONS = """
int secp256k1_ecdh(
  const secp256k1_context* ctx,
  unsigned char *result,
  const secp256k1_pubkey *pubkey,
  const unsigned char *privkey,
  void *hashfp,
  void *data
);
"""

ffi = FFI()

ffi.cdef(BASE_DEFINITIONS)
ffi.cdef(EXTRAKEYS_DEFINITIONS)
ffi.cdef(RECOVERY_DEFINITIONS)
ffi.cdef(SCHNORRSIG_DEFINITIONS)
ffi.cdef(ECDH_DEFINITIONS)

here = os.path.dirname(os.path.abspath(__file__))
lib = ffi.dlopen(os.path.join(here, 'libsecp256k1.dll'))
