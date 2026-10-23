---
name: shoaky-kotlin-style
description: Apply Shoaky's Kotlin/Spring persistence, API documentation, and caching conventions. Use when writing or reviewing Kotlin, Spring Boot, Spring MVC Controllers, OpenAPI schemas, JPA entities, DTOs/views, Flyway migrations, or cache-backed readers.
---

# Shoaky Kotlin Style

Apply every relevant rule before considering an implementation complete.

## Kotlin Functions

- Give every implemented function an explicit block body with braces.
- Use an explicit `return` in non-`Unit` functions.
- Keep abstract interface methods as declarations without artificial bodies.
- Use plain primary-constructor injection in production Kotlin classes and omit constructor-level `@Autowired`.
- Use `@Autowired lateinit var` field injection in Spring test classes instead of constructor injection.
- Never use Kotlin's non-null assertion operator (`!!`). Use `requireNotNull`, a safe call, or an explicit branch so the invariant and failure mode remain visible.

```kotlin
fun findById(id: String): Realm? {
    return repository.findById(id).orElse(null)
}
```

## Time Durations

- Model Kotlin timeout, delay, interval, TTL, and other elapsed-time values with `kotlin.time.Duration`, not numeric fields whose names encode units such as `timeoutMillis` or `delaySeconds`.
- Name a duration property by its meaning, such as `timeout` or `retryDelay`; construct values explicitly with `500.milliseconds`, `2.seconds`, or another `Duration` unit.
- Keep `Duration` across internal interfaces and coroutine calls. Convert only at an external protocol or library seam that requires a numeric unit, and make that conversion explicit at the seam.

## Visibility

- Declare Spring Controller classes as top-level `private` classes.
- When the Model Depth rules justify a controller-only request or response DTO, define it as a nested class inside the top-level `private` Controller; the private enclosing type already prevents external access.
- Increase visibility only when another production file requires the type.

## Persistence IDs

- Choose the primary-key strategy from the deployment model before defining the Kotlin ID type.
- For low-volume tables that do not need distributed ID generation or insertion locality, use a database-generated UUIDv4.
- For a single-node deployment with a large data volume, use a database-generated auto-incrementing integer ID, normally `bigint`/`Long`.
- For a distributed deployment, use UUIDv7 so IDs can be generated independently while retaining time ordering.
- Store UUID identifiers and logical relationship IDs as `varchar(36)` when Kotlin models expose them as `String`, avoiding custom UUID mapping components.
- Let PostgreSQL generate auto-incrementing IDs, UUIDv4 IDs, or UUIDv7 IDs according to the selected strategy.
- Prefer the database's native UUIDv7 function. On PostgreSQL versions without one, provide a migration-owned compatible generator instead of falling back to UUIDv4 or application-side generation.
- Model a new JPA entity ID as nullable because it has no ID before insertion, using `Long?` for auto-incrementing IDs or `String?` for UUID string IDs.
- Use Hibernate database-generated value support so the generated ID is read back after insertion.
- Use the corresponding non-null ID type at repository lookup, domain operation, and cache interfaces.

## Database Relationships

- Represent relationships with logical ID columns only; do not create database foreign-key constraints.
- Do not use JPA object relationship mappings to recreate database coupling when plain ID fields are sufficient.
- Keep indexes required by relationship lookups and business queries.
- Enforce relationship existence, tenant/realm consistency, deletion checks, and cleanup in application services or explicit jobs.
- Do not rely on database `ON DELETE CASCADE` or `ON DELETE RESTRICT`; define and test deletion behavior in application code.

## SQL Constraint Style

- Declare a single-column primary key directly on its column with `PRIMARY KEY`; do not add a separate table-level `CONSTRAINT pk_* PRIMARY KEY` declaration.
- Keep composite primary keys as named table-level constraints, such as `CONSTRAINT pk_example PRIMARY KEY (first_id, second_id)`.
- Make every DDL migration idempotent: use `CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`, and `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`.
- Guard PostgreSQL constraint additions through `pg_constraint` because `ADD CONSTRAINT IF NOT EXISTS` is unsupported, and make seed inserts conflict-safe.

## Persistence Queries

- Prefer extending entity repositories with `JpaSpecificationExecutor` so composable filtering does not produce a growing set of derived Repository methods.
- Build Specifications inside the owning Manager from domain query inputs; Controllers and Services must not construct persistence predicates.
- Reference entity attributes in Specifications with Kotlin property names such as `ClientEntity::clientId.name` instead of raw strings. Use an explicit string only when the path is not a camel-case entity property or cannot be expressed as a property reference.
- Apply the same property-reference rule to entity-backed sorting, such as `Sort.by(ClientEntity::createdAt.name)`.
- Keep explicit Repository methods for stable semantic queries such as pessimistic locks, cross-entity projections, and fixed relationship traversals where a Specification would obscure intent.
- Do not add a Specification for a primary-key lookup already provided by `JpaRepository`.

## Layered Repository Boundaries For Core Modules

This is a general layering and boundary-design technique. It is independent of Spring, MongoDB, or any other software framework. Apply it when the architecture deliberately separates reusable core logic from the application layer; it is not the default style for every module or every query.

- Define the repository interface inside the core module as the smallest capability seam required by core algorithms and invariants. Do not turn it into a catalog of application searches, pagination, reporting, administration, or UI queries.
- Implement that core interface in the application layer with an adapter such as `CommandDataRepo`. The adapter may compose a persistence-native repository with lower-level persistence operations to implement core-required saves, lookups, and atomic conditional updates.
- Keep the persistence-native repository, such as `CommandDataMongoRepository`, available to application business code. Application-only queries should use its native query, paging, sorting, and extension capabilities directly instead of expanding the core repository interface.
- Use two deliberate access paths: core logic calls its minimal repository interface through the application adapter; application-specific query logic calls the persistence-native repository. Do not add pass-through methods to the core interface merely to hide the native repository from application code.
- Promote a query into the core repository interface only when a core algorithm, invariant, or state transition requires it. A query needed only by an application service, controller, operator view, or report remains outside the core interface.
- Keep application access to the native repository from bypassing core-owned writes, atomic transitions, lifecycle cleanup, authorization or tenant rules, transaction ordering, and cache consistency. If an operation can violate one of those invariants, route it through the owning core/application adapter instead of querying or mutating the native repository directly.
- Do not apply this split mechanically to normal business modules. When one business module owns the entity, cache, write invariants, and lifecycle, keep callers behind that module's Manager/Service interface as specified elsewhere in this skill.

Reference pattern: `CommandDataRepository` is the minimal core seam; application-layer `CommandDataRepo` implements it; `CommandApplication` uses `CommandDataMongoRepository` directly for application-only retrieval and paged queries.

## Model Depth

- Name every JPA database entity class with an `Entity` suffix, such as `RealmEntity`.
- Keep domain and API terminology free of the technical `Entity` suffix.
- Keep derived activity or status data out of metadata entities unless a confirmed read requirement and measured performance constraint justify denormalization.
- Return the entity or domain type directly when the caller needs exactly the same fields.
- Introduce a DTO or View only when its fields, security exposure, aggregation, or representation differ.
- Do not create DTO/Response/Snapshot/View wrappers that copy an entity or domain type one-to-one.
- Keep the smallest correct set of classes and mappings.

## Module Dependency Direction

- Keep dependency direction aligned with relationship ownership. The module that owns the starting relationship resolves its IDs, then calls the downstream module through its Manager interface.
- Keep leaf modules focused on relationships between their own models. Accept owned IDs from callers instead of injecting upstream services solely to discover those IDs.
- Treat nested resources as part of the parent aggregate's application interface. Their Controllers call the parent Service, which validates the parent and delegates persistence to the child Manager.
- Keep a child resource Manager independent of the parent module. It may store and filter by the parent's logical ID, but it must not inject, load, or validate the parent; that policy belongs to the parent Service.
- Introduce a higher-level `Manager` only when orchestration spans multiple peer modules and no single module owns the traversal. Do not add a pass-through Manager when a relationship owner already provides the natural seam.
- For example, a Role Service resolves User-to-Role and Role-to-Permission relationships, then passes Permission IDs to a Permission Manager to obtain control points; the Permission module must not depend back on User or Role services.

## Module Naming And Standard Protocols

- Name a module from its actual responsibility, not from the fact that Spring manages it.
- Keep Spring dependency flow as Controller to Service to Manager. A Service must not inject another Service; expose reusable downstream capabilities through a role-specific Manager instead.
- Reserve `Service` for business operations and orchestration. Use role-specific names such as `Manager`, `Codec`, `Validator`, `Client`, or `Provider` for infrastructure and protocol modules, and use the matching Spring stereotype such as `@Component` when they are not business services.
- A JWT signing and verification module is a protocol/infrastructure module, so prefer a name such as `JwtTokenManager` rather than `JwtTokenService`.
- Use a mature third-party library for standard security protocols and formats such as JWT/JWS, OAuth 2.0, and OIDC. Do not manually implement token serialization, parsing, signing envelopes, or protocol validation when a maintained library provides them.
- Keep custom code focused on application policy and integration: Realm issuer rules, claim selection, key loading, Session checks, and business error mapping.
- Keep security tokens minimal. Every custom claim must have a concrete consumer; do not duplicate data already represented by a standard claim or persisted relationship.

## Schema Documentation

- Annotate database entity classes and every API-exposed request or response model with `io.swagger.v3.oas.annotations.media.Schema`, including DTO, View, and directly returned domain types.
- Annotate their fields with `@field:Schema`, including a useful description and examples where they clarify format or units.
- Mark generated IDs and timestamps as read-only in Schema metadata.
- Annotate every Spring MVC endpoint with `@Operation`. Give each operation a stable, explicitly declared, globally unique `operationId`, a concise `summary`, and a `description` sufficient for a generated client or LLM to understand the purpose, inputs, outputs, preconditions, security-sensitive behavior, and business side effects without reading the implementation.
- Mark request-only secrets as write-only and one-time or response-only secrets as read-only in Schema metadata. State when a sensitive value is returned only once and when clients must prevent caching.
- Verify the generated `/v3/api-docs` document in an integration test. Every HTTP operation must have a non-blank `operationId`, `summary`, and `description`, and operation IDs must be unique.
- Add Chinese PostgreSQL `COMMENT ON TABLE` and `COMMENT ON COLUMN` statements for every migrated table and column.

## Schema Confirmation Gate

- Before implementing a new persistence module or changing its schema, present every proposed table for explicit user confirmation.
- Include each column's type, nullability, default, and purpose, plus indexes, unique constraints, logical relationships, application-level delete behavior, and cache impact.
- Call out assumptions and unresolved domain choices instead of guessing.
- Wait for explicit confirmation before writing Flyway migrations, entities, repositories, or schema-dependent business code.
- Treat a requested adjustment as a new proposal and repeat the confirmation gate before implementation.

## Timestamps And Validation

- Keep business-field defaults in the Kotlin entity constructor as the single source of truth.
- Do not give a business `String` field an empty-string default unless the empty value has an explicit domain meaning. Require callers to provide the value or model absence as nullable instead.
- Do not duplicate business defaults in Flyway column definitions.
- Allow database defaults only for `created_at` and database-generated identifiers; seed rows must state required business values explicitly.
- Make `created_at` non-null with the current time by default.
- Keep `updated_at` nullable with a database default of `NULL`; populate it only on the first update.
- Prefer assigning `updatedAt = Instant.now()` explicitly in the business update path. Avoid JPA lifecycle callbacks such as `@PreUpdate`, which hide when timestamps change.
- Encode confirmed invariants as database constraints.
- Do not invent strict formats or validation rules for names, codes, or identifiers without an explicit business requirement.

## Caching

- Use local Caffeine caches unless a task explicitly chooses another backend.
- Use Spring Cache annotations for all production cache reads and writes. Domain services and managers must not inject `CacheManager` or call cache `get`, `put`, `evict`, or `clear` methods directly.
- Configure the Spring `CacheManager` as transaction-aware so ordinary annotation-driven puts and evictions occur only after a successful transaction commit.
- Use only the relevant domain ID as the variable cache key. Never key cached domain objects by name, username, code, query criteria, or a composite business key.
- Resolve alternate identifiers through the database, then cache the domain read by ID.
- Put `@Cacheable` on ID-based reads and return the existing entity/domain type unless a distinct read model is justified.
- On transactional updates and deletes, use `@Caching` with two `@CacheEvict` operations for each affected ID: one with `beforeInvocation = true` to close the stale-repopulation window and one ordinary eviction that the transaction-aware cache defers until commit. Treat the database as the source of truth.
- Account for Spring proxy boundaries. When a cached write is invoked through self-invocation, move it behind another bean or annotate the externally invoked aggregate operation; use `allEntries = true` only when its affected ID keys cannot be expressed individually.
- The module that owns an entity and its cache must expose all read and write operations through its own manager/service interface, including create, update, delete, locked reads, and cache eviction.
- Cross-module callers must not inject the owning module's repository or `CacheManager` to bypass that interface. Keep persistence and cache-consistency knowledge inside the owning module.
- Put cache annotations on the owning module's write methods so callers cannot forget invalidation.

## Completion Check

Before finishing, verify modified Kotlin and persistence code against every applicable rule above. Choose verification from the actual change and its risk; do not mechanically run or add tests for every task.

- Add or update tests only when the change introduces or alters observable behavior, fixes a regression that needs protection, changes persistence semantics, or otherwise has a meaningful contract not already covered. Do not add tests for formatting, translations, comments, mechanical wiring, or implementation-only changes whose behavior is already covered.
- Run the narrowest existing test, build target, compiler task, inspection, or executable scenario that can detect a plausible defect in the change. A full project build or broad test suite is not required unless the change has project-wide impact or narrower verification is unavailable.
- If unrelated repository failures prevent the selected verification, report the exact blocker; do not modify unrelated code or replace the failed check with a misleading success claim.
- Create a local Git commit only when the user explicitly requests one. Use the repository's commit convention and include only files changed for the task.
